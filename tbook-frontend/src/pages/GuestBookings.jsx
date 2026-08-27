import { useEffect, useState } from 'react';
import { bookingApi, reviewApi } from '../api/endpoints';
import { apiErrorMessage } from '../api/client';
import { Spinner, Empty, ErrorBanner, SuccessBanner, StatusStamp, ConfirmButton, Modal } from '../components/Common';
import BookingDetailModal from '../components/BookingDetail';
import { BOOKING_STATUS_LABELS } from '../constants';
import { StarIcon, PencilIcon, TrashIcon } from '../components/Icons';

const TABS = [
  { key: 'active', label: 'Active', loader: bookingApi.active },
  { key: 'completed', label: 'Completed', loader: bookingApi.completed },
  { key: 'cancelled', label: 'Cancelled/Rejected', loader: bookingApi.cancelledRejected },
  { key: 'all', label: 'All', loader: bookingApi.all },
];

export default function GuestBookings() {
  const [section, setSection] = useState('bookings');

  return (
    <div>
      <p className="eyebrow">My Account</p>
      <h1>{section === 'bookings' ? 'My Bookings' : 'My Reviews'}</h1>

      <div className="tabs">
        <button className={`tab${section === 'bookings' ? ' active' : ''}`} onClick={() => setSection('bookings')}>
          Bookings
        </button>
        <button className={`tab${section === 'reviews' ? ' active' : ''}`} onClick={() => setSection('reviews')}>
          Reviews
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
      .catch((err) => setError(apiErrorMessage(err, 'Failed to load bookings.')))
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
      setNotice('Booking cancelled.');
      load();
    } catch (err) {
      setError(apiErrorMessage(err, 'Failed to cancel the booking.'));
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
        <Empty title="Nothing here yet" hint="Book a place in the catalog to see it here." />
      )}

      {!loading && items && items.length > 0 && (
        <div className="row-list">
          {items.map((b) => (
            <div className="row-item" key={b.uuid}>
              <div className="row-main">
                <span className="row-title">{b.property_title}{b.unit_title ? ` — ${b.unit_title}` : ''}</span>
                <span className="row-meta">
                  {b.check_in} → {b.check_out} · {b.number_of_guests} guests · {b.total_price} €
                </span>
              </div>
              <div className="row-actions">
                <StatusStamp status={b.status} labels={BOOKING_STATUS_LABELS} />
                <button className="btn btn-secondary btn-sm" onClick={() => setDetailTarget(b.uuid)}>
                  Details
                </button>
                {b.status === 'pending' || b.status === 'confirmed' ? (
                  <ConfirmButton label="Cancel" confirmLabel="Cancel booking?" onConfirm={() => cancelBooking(b.uuid)} />
                ) : null}
                {b.status === 'completed' && (
                  <button className="btn btn-secondary btn-sm" onClick={() => setReviewTarget(b)}>
                    Leave a review
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
          onDone={() => { setReviewTarget(null); setNotice('Thank you for your review!'); }}
        />
      )}

      {detailTarget && (
        <BookingDetailModal
          title="Booking Details"
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
      .catch((err) => setError(apiErrorMessage(err, 'Failed to load reviews.')))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
  }, []);

  const removeReview = async (uuid) => {
    setNotice('');
    try {
      await reviewApi.remove(uuid);
      setNotice('Review deleted.');
      load();
    } catch (err) {
      setError(apiErrorMessage(err, 'Failed to delete the review.'));
    }
  };

  return (
    <div>
      <p className="field-hint" style={{ marginTop: -18, marginBottom: 20 }}>
        Here you can edit the rating and text, or delete your review.
      </p>

      <ErrorBanner message={error} />
      <SuccessBanner message={notice} />
      {loading && <Spinner />}

      {!loading && items && items.length === 0 && (
          <Empty title="No reviews yet" hint={'Leave a review for a completed stay in the "Bookings" tab.'} />
      )}

      {!loading && items && items.length > 0 && (
        <div className="row-list">
          {items.map((r) => (
            <div className="my-review-card" key={r.uuid}>
              <div className="my-review-head">
                <div>
                  <div className="row-title">{r.property_title}</div>
                  <div className="field-hint">{new Date(r.created_at).toLocaleDateString('en-US')}</div>
                </div>
                <div className="row-actions">
                  <span className="review-rating">
                    <StarIcon />
                    <span>{r.rating}/10</span>
                  </span>
                  <button className="icon-btn" aria-label="Edit review" onClick={() => setEditTarget(r)}>
                    <PencilIcon />
                  </button>
                  <ConfirmButton
                    label={<TrashIcon />}
                    confirmLabel="Delete?"
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
          onDone={() => { setEditTarget(null); setNotice('Review updated.'); load(); }}
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
      setError(apiErrorMessage(err, 'Failed to save the review.'));
    } finally {
      setBusy(false);
    }
  };

  const title = isEdit ? `Editing review for "${review.property_title}"` : `Review for "${booking.property_title}"`;

  return (
    <Modal title={title} onClose={onClose}>
      <ErrorBanner message={error} />
      <form onSubmit={submit}>
        <div className="field">
          <label>Rating (1–10)</label>
          <input type="number" min="1" max="10" required value={rating} onChange={(e) => setRating(e.target.value)} />
        </div>
        <div className="field">
          <label>Comment</label>
          <textarea rows={4} value={comment} onChange={(e) => setComment(e.target.value)} />
        </div>
        <div className="btn-row">
          <button className="btn btn-brass" disabled={busy}>
            {busy ? 'Saving…' : isEdit ? 'Save Changes' : 'Submit Review'}
          </button>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cancel
          </button>
        </div>
      </form>
    </Modal>
  );
}
