import { useEffect, useState } from 'react';
import { bookingApi, reviewApi } from '../api/endpoints';
import { apiErrorMessage } from '../api/client';
import { Spinner, Empty, ErrorBanner, SuccessBanner, StatusStamp, ConfirmButton, Modal } from '../components/Common';
import BookingDetailModal from '../components/BookingDetail';
import { BOOKING_STATUS_LABELS } from '../constants';
import { StarIcon, PencilIcon, TrashIcon } from '../components/Icons';

const TABS = [
  { key: 'active', label: 'Активные', loader: bookingApi.active },
  { key: 'completed', label: 'Завершённые', loader: bookingApi.completed },
  { key: 'cancelled', label: 'Отменённые/отклонённые', loader: bookingApi.cancelledRejected },
  { key: 'all', label: 'Все', loader: bookingApi.all },
];

export default function GuestBookings() {
  const [section, setSection] = useState('bookings');

  return (
    <div>
      <p className="eyebrow">Личный кабинет</p>
      <h1>{section === 'bookings' ? 'Мои бронирования' : 'Мои отзывы'}</h1>

      <div className="tabs">
        <button className={`tab${section === 'bookings' ? ' active' : ''}`} onClick={() => setSection('bookings')}>
          Бронирования
        </button>
        <button className={`tab${section === 'reviews' ? ' active' : ''}`} onClick={() => setSection('reviews')}>
          Отзывы
        </button>
      </div>

      {section === 'bookings' ? <BookingsSection /> : <MyReviewsSection />}
    </div>
  );
}

function BookingsSection() {
  const [tab, setTab] = useState('active');
  const [items, setItems] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [reviewTarget, setReviewTarget] = useState(null);
  const [detailTarget, setDetailTarget] = useState(null);

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
                <button className="btn btn-secondary btn-sm" onClick={() => setDetailTarget(b.uuid)}>
                  Подробнее
                </button>
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
        <ReviewModal
          booking={reviewTarget}
          onClose={() => setReviewTarget(null)}
          onDone={() => { setReviewTarget(null); setNotice('Спасибо за отзыв!'); }}
        />
      )}

      {detailTarget && (
        <BookingDetailModal
          title="Детали бронирования"
          loadDetail={() => bookingApi.detail(detailTarget)}
          onClose={() => setDetailTarget(null)}
        />
      )}
    </div>
  );
}

function MyReviewsSection() {
  const [items, setItems] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [editTarget, setEditTarget] = useState(null);

  const load = () => {
    setLoading(true);
    setError('');
    reviewApi
      .list()
      .then(({ data }) => setItems(data.results ?? data))
      .catch((err) => setError(apiErrorMessage(err, 'Не удалось загрузить отзывы.')))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
  }, []);

  const removeReview = async (uuid) => {
    setNotice('');
    try {
      await reviewApi.remove(uuid);
      setNotice('Отзыв удалён.');
      load();
    } catch (err) {
      setError(apiErrorMessage(err, 'Не удалось удалить отзыв.'));
    }
  };

  return (
    <div>
      <p className="field-hint" style={{ marginTop: -18, marginBottom: 20 }}>
        Здесь можно отредактировать оценку и текст, или удалить свой отзыв.
      </p>

      <ErrorBanner message={error} />
      <SuccessBanner message={notice} />
      {loading && <Spinner />}

      {!loading && items && items.length === 0 && (
        <Empty title="Пока нет отзывов" hint="Оставьте отзыв о завершённом проживании во вкладке «Бронирования»." />
      )}

      {!loading && items && items.length > 0 && (
        <div className="row-list">
          {items.map((r) => (
            <div className="my-review-card" key={r.uuid}>
              <div className="my-review-head">
                <div>
                  <div className="row-title">{r.property_title}</div>
                  <div className="field-hint">{new Date(r.created_at).toLocaleDateString('ru-RU')}</div>
                </div>
                <div className="row-actions">
                  <span className="review-rating">
                    <StarIcon />
                    <span>{r.rating}/10</span>
                  </span>
                  <button className="icon-btn" aria-label="Редактировать отзыв" onClick={() => setEditTarget(r)}>
                    <PencilIcon />
                  </button>
                  <ConfirmButton
                    label={<TrashIcon />}
                    confirmLabel="Удалить?"
                    onConfirm={() => removeReview(r.uuid)}
                    className="icon-btn danger"
                  />
                </div>
              </div>
              {r.comment && <p className="review-text" style={{ margin: 0 }}>{r.comment}</p>}
            </div>
          ))}
        </div>
      )}

      {editTarget && (
        <ReviewModal
          review={editTarget}
          onClose={() => setEditTarget(null)}
          onDone={() => { setEditTarget(null); setNotice('Отзыв обновлён.'); load(); }}
        />
      )}
    </div>
  );
}

// Handles both creating a new review (pass `booking`) and editing an existing
// one (pass `review`) — reviews can only be edited or deleted by their author.
function ReviewModal({ booking, review, onClose, onDone }) {
  const isEdit = !!review;
  const [rating, setRating] = useState(review?.rating ?? 10);
  const [comment, setComment] = useState(review?.comment ?? '');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    setError('');
    try {
      if (isEdit) {
        await reviewApi.update(review.uuid, { rating: Number(rating), comment });
      } else {
        await reviewApi.create({ booking: booking.uuid, rating: Number(rating), comment });
      }
      onDone();
    } catch (err) {
      setError(apiErrorMessage(err, 'Не удалось сохранить отзыв.'));
    } finally {
      setBusy(false);
    }
  };

  const title = isEdit ? `Редактирование отзыва о «${review.property_title}»` : `Отзыв о «${booking.property_title}»`;

  return (
    <Modal title={title} onClose={onClose}>
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
            {busy ? 'Сохраняем…' : isEdit ? 'Сохранить изменения' : 'Отправить отзыв'}
          </button>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Отмена
          </button>
        </div>
      </form>
    </Modal>
  );
}
