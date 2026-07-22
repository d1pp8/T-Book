import { useEffect, useState } from 'react';
import { ownerBookingApi } from '../api/endpoints';
import { apiErrorMessage } from '../api/client';
import { Spinner, Empty, ErrorBanner, SuccessBanner, StatusStamp, ConfirmButton } from '../components/Common';
import { BOOKING_STATUS_LABELS } from '../constants';

const TABS = [
  { key: 'active', label: 'Активные', loader: ownerBookingApi.active },
  { key: 'pending', label: 'Ожидают', loader: ownerBookingApi.pending },
  { key: 'confirmed', label: 'Подтверждённые', loader: ownerBookingApi.confirmed },
  { key: 'completed', label: 'Завершённые', loader: ownerBookingApi.completed },
  { key: 'cancelled', label: 'Отменённые/отклонённые', loader: ownerBookingApi.cancelledRejected },
  { key: 'all', label: 'Все', loader: ownerBookingApi.all },
];

export default function OwnerBookings() {
  const [tab, setTab] = useState('pending');
  const [items, setItems] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [busyUuid, setBusyUuid] = useState('');

  const load = () => {
    setLoading(true);
    setError('');
    const tabDef = TABS.find((t) => t.key === tab);
    tabDef
      .loader()
      .then(({ data }) => setItems(data.results ?? data))
      .catch((err) => setError(apiErrorMessage(err, 'Не удалось загрузить бронирования.')))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tab]);

  const act = async (action, uuid, doneMsg) => {
    setBusyUuid(uuid);
    setNotice('');
    setError('');
    try {
      await action(uuid);
      setNotice(doneMsg);
      load();
    } catch (err) {
      setError(apiErrorMessage(err, 'Действие не выполнено.'));
    } finally {
      setBusyUuid('');
    }
  };

  return (
    <div>
      <p className="eyebrow">Кабинет владельца</p>
      <h1>Заявки на бронирование</h1>

      <div className="tabs">
        {TABS.map((t) => (
          <button key={t.key} className={`tab${tab === t.key ? ' active' : ''}`} onClick={() => setTab(t.key)}>
            {t.label}
          </button>
        ))}
      </div>

      <ErrorBanner message={error} />
      <SuccessBanner message={notice} />
      {loading && <Spinner />}

      {!loading && items && items.length === 0 && (
        <Empty title="Здесь пока пусто" hint="Заявки на бронирование появятся здесь." />
      )}

      {!loading && items && items.length > 0 && (
        <div className="row-list">
          {items.map((b) => (
            <div className="row-item" key={b.uuid}>
              <div className="row-main">
                <span className="row-title">{b.property_title}{b.unit_title ? ` — ${b.unit_title}` : ''}</span>
                <span className="row-meta">
                  {b.user?.full_name || b.user?.email} · {b.check_in} → {b.check_out} · {b.number_of_guests} гостей · {b.total_price} ₽
                </span>
              </div>
              <div className="row-actions">
                <StatusStamp status={b.status} labels={BOOKING_STATUS_LABELS} />
                {b.status === 'pending' && (
                  <>
                    <button className="btn btn-brass btn-sm" disabled={busyUuid === b.uuid} onClick={() => act(ownerBookingApi.confirm, b.uuid, 'Бронирование подтверждено.')}>
                      Подтвердить
                    </button>
                    <ConfirmButton label="Отклонить" confirmLabel="Точно отклонить?" onConfirm={() => act(ownerBookingApi.reject, b.uuid, 'Бронирование отклонено.')} />
                  </>
                )}
                {b.status === 'confirmed' && (
                  <button className="btn btn-secondary btn-sm" disabled={busyUuid === b.uuid} onClick={() => act(ownerBookingApi.complete, b.uuid, 'Бронирование завершено.')}>
                    Завершить
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
