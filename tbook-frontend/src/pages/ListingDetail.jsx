import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { listingsApi, bookingApi } from '../api/endpoints';
import { apiErrorMessage } from '../api/client';
import { Spinner, ErrorBanner, SuccessBanner } from '../components/Common';
import { useAuth } from '../AuthContext';
import { PROPERTY_TYPES, labelFor } from '../constants';

export default function ListingDetail() {
  const { propertyUuid } = useParams();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [listing, setListing] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [selectedUnit, setSelectedUnit] = useState('');
  const [form, setForm] = useState({ check_in: '', check_out: '', adults: 1, children: 0, special_request: '' });
  const [bookingError, setBookingError] = useState('');
  const [bookingSuccess, setBookingSuccess] = useState('');
  const [bookingBusy, setBookingBusy] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    listingsApi
      .detail(propertyUuid)
      .then(({ data }) => {
        if (cancelled) return;
        setListing(data);
        setSelectedUnit(data.unit_uuid || data.categories?.[0]?.unit_uuid || '');
      })
      .catch((err) => !cancelled && setError(apiErrorMessage(err, 'Объект не найден.')))
      .finally(() => !cancelled && setLoading(false));
    return () => {
      cancelled = true;
    };
  }, [propertyUuid]);

  const submitBooking = async (e) => {
    e.preventDefault();
    setBookingError('');
    setBookingSuccess('');
    if (!isAuthenticated) {
      navigate('/login', { state: { from: { pathname: `/listings/${propertyUuid}` } } });
      return;
    }
    if (!selectedUnit) {
      setBookingError('Выберите номер/юнит для бронирования.');
      return;
    }
    setBookingBusy(true);
    try {
      await bookingApi.create({ unit: selectedUnit, ...form });
      setBookingSuccess('Бронирование создано и ожидает подтверждения владельца.');
      setForm({ check_in: '', check_out: '', adults: 1, children: 0, special_request: '' });
    } catch (err) {
      setBookingError(apiErrorMessage(err, 'Не удалось создать бронирование.'));
    } finally {
      setBookingBusy(false);
    }
  };

  if (loading) return <Spinner />;
  if (error) return <ErrorBanner message={error} />;
  if (!listing) return null;

  return (
    <div>
      <p className="eyebrow">{labelFor(PROPERTY_TYPES, listing.type)}</p>
      <h1>{listing.title}</h1>
      <p className="subtitle">
        {listing.address?.street} {listing.address?.house_number}, {listing.address?.city}, {listing.address?.country}
        {' · '}★ {listing.rating} ({listing.review_count} отзывов)
      </p>

      {listing.gallery?.length > 0 && (
        <div className="gallery" style={{ marginBottom: 28 }}>
          {listing.gallery.map((src) => (
            <div className="gallery-item" key={src} style={{ width: 160, height: 120 }}>
              <img src={src} alt={listing.title} />
            </div>
          ))}
        </div>
      )}

      <div className="two-col">
        <div>
          <h3>Описание</h3>
          <p>{listing.description}</p>

          {listing.amenities?.length > 0 && (
            <>
              <h3>Удобства</h3>
              <div className="checkbox-grid" style={{ marginBottom: 24 }}>
                {listing.amenities.map((a) => (
                  <span className="chip" key={a.title}>
                    {a.title}
                  </span>
                ))}
              </div>
            </>
          )}

          {listing.categories?.length > 0 && (
            <>
              <h3>Варианты размещения</h3>
              <div className="row-list" style={{ marginBottom: 24 }}>
                {listing.categories.map((cat) => (
                  <label
                    key={cat.unit_uuid}
                    className="row-item"
                    style={{ cursor: 'pointer', borderColor: selectedUnit === cat.unit_uuid ? 'var(--brass)' : undefined }}
                  >
                    <div className="row-main">
                      <span className="row-title">{cat.title}</span>
                      <span className="row-meta">
                        {cat.guests_from}–{cat.guests_to} гостей · {cat.area_from}–{cat.area_to} м² · доступно {cat.units_available}
                      </span>
                    </div>
                    <div className="row-actions">
                      <span className="price">{cat.price_from}–{cat.price_to} ₽/ночь</span>
                      <input
                        type="radio"
                        name="unit"
                        checked={selectedUnit === cat.unit_uuid}
                        onChange={() => setSelectedUnit(cat.unit_uuid)}
                      />
                    </div>
                  </label>
                ))}
              </div>
            </>
          )}

          <h3>Отзывы</h3>
          {listing.reviews?.length ? (
            <div className="row-list">
              {listing.reviews.map((r) => (
                <div className="card card-pad" key={r.uuid}>
                  <div className="row-title">{r.user} — ★ {r.rating}/10</div>
                  <p style={{ marginBottom: 0 }}>{r.comment}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="field-hint">Пока нет отзывов.</p>
          )}
        </div>

        <div className="card card-pad side-card">
          <h3>Забронировать</h3>
          <ErrorBanner message={bookingError} />
          <SuccessBanner message={bookingSuccess} />
          <form onSubmit={submitBooking}>
            <div className="field-row">
              <div className="field">
                <label>Заезд</label>
                <input type="date" required value={form.check_in} onChange={(e) => setForm({ ...form, check_in: e.target.value })} />
              </div>
              <div className="field">
                <label>Выезд</label>
                <input type="date" required value={form.check_out} onChange={(e) => setForm({ ...form, check_out: e.target.value })} />
              </div>
            </div>
            <div className="field-row">
              <div className="field">
                <label>Взрослые</label>
                <input type="number" min="1" required value={form.adults} onChange={(e) => setForm({ ...form, adults: e.target.value })} />
              </div>
              <div className="field">
                <label>Дети</label>
                <input type="number" min="0" value={form.children} onChange={(e) => setForm({ ...form, children: e.target.value })} />
              </div>
            </div>
            <div className="field">
              <label>Пожелания (необязательно)</label>
              <textarea rows={3} value={form.special_request} onChange={(e) => setForm({ ...form, special_request: e.target.value })} />
            </div>
            <button className="btn btn-brass" style={{ width: '100%' }} disabled={bookingBusy}>
              {bookingBusy ? 'Отправляем…' : isAuthenticated ? 'Забронировать' : 'Войдите, чтобы забронировать'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
