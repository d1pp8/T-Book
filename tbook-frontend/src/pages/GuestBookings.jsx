import { useEffect, useState } from 'react';
import { bookingApi, reviewApi } from '../api/endpoints';
import { apiErrorMessage } from '../api/client';
import { Spinner, Empty, ErrorBanner, SuccessBanner, StatusStamp, ConfirmButton, Modal } from '../components/Common';
import { BOOKING_STATUS_LABELS } from '../constants';

const TABS = [
  { key: 'active', label: 'Активные', loader: bookingApi.active },
  { key: 'completed', label: 'Завершённые', loader: bookingApi.completed },
  { key: 'cancelled', label: 'Отменённые/отклонённые', loader: bookingApi.cancelledRejected },
  { key: 'all', label: 'Все', loader: bookingApi.all },
];

export default function GuestBookings() {
  const [tab, setTab] = useState('active');
  const [items, setItems] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [reviewTarget, setReviewTarget] = useState(null);

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

  const cancelBooking = async (uuid) => {
    setNotice('');
    try {
      await bookingApi.cancel(uuid);
      setNotice('Бронирование отменено.');
      load();
    } catch (err) {
      setError(apiErrorMessage(err, 'Не удалось отменить бронирование.'));
    }
  };

  return (
    <div>
      <p className="eyebrow">Личный кабинет</p>
      <h1>Мои бронирования</h1>

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
        <Empty title="Здесь пока пусто" hint="Забронируйте жильё в каталоге, чтобы увидеть его тут." />
      )}

      {!loading && items && items.length > 0 && (
        <div className="row-list">
          {items.map((b) => (
            <div className="row-item" key={b.uuid}>
              <div className="row-main">
                <span className="row-title">{b.property_title}{b.unit_title ? ` — ${b.unit_title}` : ''}</span>
                <span className="row-meta">
                  {b.check_in} → {b.check_out} · {b.number_of_guests} гостей · {b.total_price} €
                </span>
              </div>
              <div className="row-actions">
                <StatusStamp status={b.status} labels={BOOKING_STATUS_LABELS} />
                {b.status === 'pending' || b.status === 'confirmed' ? (
                  <ConfirmButton label="Отменить" confirmLabel="Отменить бронь?" onConfirm={() => cancelBooking(b.uuid)} />
                ) : null}
                {b.status === 'completed' && (
                  <button className="btn btn-secondary btn-sm" onClick={() => setReviewTarget(b)}>
                    Оставить отзыв
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {reviewTarget && (
        <ReviewModal booking={reviewTarget} onClose={() => setReviewTarget(null)} onDone={() => { setReviewTarget(null); setNotice('Спасибо за отзыв!'); }} />
      )}
    </div>
  );
}

function ReviewModal({ booking, onClose, onDone }) {
  const [rating, setRating] = useState(10);
  const [comment, setComment] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    setError('');
    try {
      await reviewApi.create({ booking: booking.uuid, rating: Number(rating), comment });
      onDone();
    } catch (err) {
      setError(apiErrorMessage(err, 'Не удалось сохранить отзыв.'));
    } finally {
      setBusy(false);
    }
  };

  return (
    <Modal title={`Отзыв о «${booking.property_title}»`} onClose={onClose}>
      <ErrorBanner message={error} />
      <form onSubmit={submit}>
        <div className="field">
          <label>Оценка (1–10)</label>
          <input type="number" min="1" max="10" required value={rating} onChange={(e) => setRating(e.target.value)} />
        </div>
        <div className="field">
          <label>Комментарий</label>
          <textarea rows={4} value={comment} onChange={(e) => setComment(e.target.value)} />
        </div>
        <div className="btn-row">
          <button className="btn btn-brass" disabled={busy}>
            {busy ? 'Отправляем…' : 'Отправить отзыв'}
          </button>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Отмена
          </button>
        </div>
      </form>
    </Modal>
  );
}
