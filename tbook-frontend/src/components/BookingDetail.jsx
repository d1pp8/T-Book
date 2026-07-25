import { useEffect, useState } from 'react';
import { apiErrorMessage } from '../api/client';
import { Modal, Spinner, ErrorBanner, StatusStamp } from './Common';
import { BOOKING_STATUS_LABELS } from '../constants';

// Fetches and shows the full booking record (duration, can_cancel, price
// breakdown, special_request, and — for owners — the guest's contact info).
// `loadDetail` is the API call bound to this booking's uuid, e.g.
// () => bookingApi.detail(uuid) or () => ownerBookingApi.detail(uuid).
export default function BookingDetailModal({ title, loadDetail, onClose, isOwnerView = false }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError('');
    loadDetail()
      .then(({ data }) => !cancelled && setData(data))
      .catch((err) => !cancelled && setError(apiErrorMessage(err, 'Не удалось загрузить бронирование.')))
      .finally(() => !cancelled && setLoading(false));
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Modal title={title || 'Бронирование'} onClose={onClose}>
      <ErrorBanner message={error} />
      {loading && <Spinner />}

      {!loading && data && (
        <div className="row-list" style={{ gap: 10 }}>
          <div className="row-main" style={{ marginBottom: 4 }}>
            <StatusStamp status={data.status} labels={BOOKING_STATUS_LABELS} />
          </div>

          {data.property && (
            <div>
              <div className="row-title">{data.property.title}</div>
              <div className="field-hint">
                {data.property.city}, {data.property.country}, {data.property.street} {data.property.house_number}
              </div>
            </div>
          )}

          {data.unit && (
            <div className="field-hint">
              Номер/юнит: <strong>{data.unit.title || 'Без названия'}</strong>
              {data.unit.room_number ? ` (№${data.unit.room_number})` : ''}
            </div>
          )}

          {isOwnerView && data.user && (
            <div className="field-hint">
              Гость: <strong>{data.user.full_name || data.user.email}</strong>
              {data.user.email ? ` · ${data.user.email}` : ''}
              {data.user.phone ? ` · ${data.user.phone}` : ''}
            </div>
          )}

          <div className="field-row">
            <div className="field-hint">Заезд: <strong>{data.check_in}</strong></div>
            <div className="field-hint">Выезд: <strong>{data.check_out}</strong></div>
          </div>
          <div className="field-row">
            <div className="field-hint">Ночей: <strong>{data.duration}</strong></div>
            <div className="field-hint">Гостей: <strong>{data.adults} взр. {data.children ? `+ ${data.children} дет.` : ''}</strong></div>
          </div>
          <div className="field-row">
            <div className="field-hint">Цена/ночь: <strong>{data.price_per_night} €</strong></div>
            <div className="field-hint">Итого: <strong>{data.total_price} €</strong></div>
          </div>

          {data.special_request && (
            <div>
              <div className="field-hint" style={{ marginBottom: 4 }}>Пожелания гостя:</div>
              <p className="body-text" style={{ marginTop: 0 }}>{data.special_request}</p>
            </div>
          )}

          <div className="field-hint">
            {String(data.can_cancel) === 'true' ? 'Бронирование ещё можно отменить.' : 'Отмена бронирования больше недоступна.'}
          </div>
        </div>
      )}
    </Modal>
  );
}
