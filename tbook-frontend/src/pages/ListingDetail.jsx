import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { listingsApi, bookingApi } from '../api/endpoints';
import { apiErrorMessage } from '../api/client';
import { Spinner, ErrorBanner, SuccessBanner } from '../components/Common';
import { useAuth } from '../AuthContext';
import { PROPERTY_TYPES, labelFor } from '../constants';
import {
  HeartRatingIcon,
  PinIcon,
  UsersIcon,
  BedIcon,
  AreaIcon,
  BathIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  StarIcon,
  ThumbUpIcon,
  ThumbDownIcon,
  AmenityDotIcon,
} from '../components/Icons';

function initials(name = '') {
  return name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((p) => p[0]?.toUpperCase())
    .join('') || '?';
}

export default function ListingDetail() {
  const { propertyUuid } = useParams();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [listing, setListing] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [heroIndex, setHeroIndex] = useState(0);
  const [unitIndex, setUnitIndex] = useState(0);
  const [unitImageIndex, setUnitImageIndex] = useState(0);

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
        const firstUnit = data.unit_uuid || data.categories?.[0]?.unit_uuid || '';
        setSelectedUnit(firstUnit);
        const idx = data.categories?.findIndex((c) => c.unit_uuid === firstUnit);
        setUnitIndex(idx > 0 ? idx : 0);
      })
      .catch((err) => !cancelled && setError(apiErrorMessage(err, 'Объект не найден.')))
      .finally(() => !cancelled && setLoading(false));
    return () => {
      cancelled = true;
    };
  }, [propertyUuid]);

  const categories = listing?.categories || [];
  const activeUnit = categories[unitIndex];
  const isSingleUnit = !categories.length && !!listing?.unit_uuid;

  useEffect(() => {
    setUnitImageIndex(0);
  }, [unitIndex]);

  const goUnit = (dir) => {
    if (!categories.length) return;
    setUnitIndex((i) => (i + dir + categories.length) % categories.length);
  };

  const goUnitImage = (dir) => {
    const len = activeUnit?.gallery?.length || 0;
    if (!len) return;
    setUnitImageIndex((i) => (i + dir + len) % len);
  };

  const pickUnit = (unit) => {
    setSelectedUnit(unit.unit_uuid);
    const el = document.getElementById('book');
    el?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

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

  const heroGallery = listing?.gallery?.length ? listing.gallery : [];
  const heroMain = heroGallery[heroIndex];

  if (loading) return <Spinner />;
  if (error) return <ErrorBanner message={error} />;
  if (!listing) return null;

  return (
    <div>
      <p className="eyebrow">{labelFor(PROPERTY_TYPES, listing.type)}</p>

      {/* ---------- Hero: gallery + owner/address/amenities ---------- */}
      <div className="hero-grid">
        <div className="hero-gallery">
          <div className="hero-gallery-main">
            {heroMain ? <img src={heroMain} alt={listing.title} /> : <div className="img-placeholder" />}
            <div className="rating-badge">
              <HeartRatingIcon size={14} />
              <span>{listing.rating}</span>
              {listing.review_count != null && <span className="rating-badge-count">({listing.review_count})</span>}
            </div>
          </div>
          {heroGallery.length > 1 && (
            <div className="hero-gallery-thumbs">
              {heroGallery.slice(0, 4).map((src, i) => (
                <button
                  key={src + i}
                  className={`hero-thumb${i === heroIndex ? ' active' : ''}`}
                  onClick={() => setHeroIndex(i)}
                  aria-label={`Фото ${i + 1}`}
                >
                  <img src={src} alt="" />
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="hero-info">
          <div className="hero-info-row">
            <span className="avatar-circle">{initials(listing.owner?.name)}</span>
            <div>
              <div className="hero-info-label">Владелец</div>
              <div className="hero-info-value">{listing.owner?.name}</div>
            </div>
          </div>

          <div className="hero-info-row">
            <span className="icon-badge">
              <PinIcon size={15} />
            </span>
            <div>
              <div className="hero-info-label">Адрес</div>
              <div className="hero-info-value">
                {listing.address?.city}, {listing.address?.street} {listing.address?.house_number}
              </div>
            </div>
          </div>

          {listing.amenities?.length > 0 && (
            <div className="hero-amenities">
              <div className="hero-info-label" style={{ marginBottom: 8 }}>
                Удобства
              </div>
              <div className="amenity-icon-row">
                {listing.amenities.map((a) => (
                  <span className="amenity-icon" key={a.title} title={a.title}>
                    {a.icon ? <img src={a.icon} alt="" /> : <AmenityDotIcon size={15} />}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="hero-title-row">
        <div>
          <h1>{listing.title}</h1>
          <p className="body-text">{listing.description}</p>
        </div>
        <a href="#book" className="btn btn-brass hero-book-btn">
          Забронировать
        </a>
      </div>

      <hr className="rule" />

      {/* ---------- Single-unit facts (apartment / villa / house — no room categories) ---------- */}
      {isSingleUnit && (
        <>
          <h2>Параметры жилья</h2>
          <div className="unit-summary-row" style={{ marginBottom: 18 }}>
            <div className="single-unit-facts">
              {listing.area != null && (
                <div className="unit-fact">
                  <AreaIcon size={15} />
                  <span>{listing.area} м²</span>
                </div>
              )}
              {listing.bedrooms != null && (
                <div className="unit-fact">
                  <BedIcon size={15} />
                  <span>{listing.bedrooms} спальни</span>
                </div>
              )}
              {listing.bathrooms != null && (
                <div className="unit-fact">
                  <BathIcon size={15} />
                  <span>{listing.bathrooms} санузла</span>
                </div>
              )}
              {listing.max_guests != null && (
                <div className="unit-fact">
                  <UsersIcon size={15} />
                  <span>до {listing.max_guests} гостей</span>
                </div>
              )}
              {listing.beds?.length > 0 && (
                <div className="unit-fact">
                  <BedIcon size={15} />
                  <span>{listing.beds.map((b) => `${b.type} ×${b.quantity}`).join(', ')}</span>
                </div>
              )}
            </div>
            <div className="unit-summary-actions">
              {listing.price_per_night != null && (
                <span className="price price-lg">
                  {listing.price_per_night} €<span className="price-label"> / ночь</span>
                </span>
              )}
              <a href="#book" className="btn btn-brass">
                Забронировать
              </a>
            </div>
          </div>
          <hr className="rule" />
        </>
      )}

      {/* ---------- Room categories browser ---------- */}
      {categories.length > 0 && (
        <>
          <h2>Номера</h2>
          <div className="unit-browser">
            <button className="unit-nav-btn" onClick={() => goUnit(-1)} disabled={categories.length < 2} aria-label="Предыдущий номер">
              <ChevronLeftIcon />
            </button>

            <div className="unit-browser-body">
              <div className="unit-gallery">
                <button className="unit-image-arrow left" onClick={() => goUnitImage(-1)} disabled={(activeUnit?.gallery?.length || 0) < 2} aria-label="Предыдущее фото">
                  <ChevronLeftIcon size={16} />
                </button>
                <div className="unit-gallery-main">
                  {activeUnit?.gallery?.[unitImageIndex] ? (
                    <img src={activeUnit.gallery[unitImageIndex]} alt={activeUnit.title} />
                  ) : (
                    <div className="img-placeholder" />
                  )}
                  <div className="guests-badge">
                    <UsersIcon size={14} />
                    <span>{activeUnit?.guests_to}</span>
                  </div>
                </div>
                <button className="unit-image-arrow right" onClick={() => goUnitImage(1)} disabled={(activeUnit?.gallery?.length || 0) < 2} aria-label="Следующее фото">
                  <ChevronRightIcon size={16} />
                </button>
                {activeUnit?.gallery?.length > 1 && (
                  <div className="unit-thumb-col">
                    {activeUnit.gallery.slice(0, 4).map((src, i) => (
                      <button
                        key={src + i}
                        className={`unit-thumb${i === unitImageIndex ? ' active' : ''}`}
                        onClick={() => setUnitImageIndex(i)}
                      >
                        <img src={src} alt="" />
                      </button>
                    ))}
                  </div>
                )}
              </div>

              <div className="unit-facts">
                {activeUnit?.beds?.length > 0 && (
                  <div className="unit-fact">
                    <BedIcon size={15} />
                    <span>{activeUnit.beds.map((b) => `${b.type} ×${b.quantity}`).join(', ')}</span>
                  </div>
                )}
                <div className="unit-fact">
                  <AreaIcon size={15} />
                  <span>
                    {activeUnit?.area_from}–{activeUnit?.area_to} м²
                  </span>
                </div>
                <div className="unit-fact">
                  <UsersIcon size={15} />
                  <span>
                    {activeUnit?.guests_from}–{activeUnit?.guests_to} гостей
                  </span>
                </div>
                {activeUnit?.amenities?.length > 0 && (
                  <div className="unit-fact-amenities">
                    {activeUnit.amenities.map((a) => (
                      <span className="chip" key={a.title}>
                        {a.icon ? <img src={a.icon} alt="" className="chip-icon" /> : <AmenityDotIcon size={12} />} {a.title}
                      </span>
                    ))}
                  </div>
                )}
                <div className="unit-fact-hint">Доступно: {activeUnit?.units_available}</div>
              </div>
            </div>

            <button className="unit-nav-btn" onClick={() => goUnit(1)} disabled={categories.length < 2} aria-label="Следующий номер">
              <ChevronRightIcon />
            </button>
          </div>

          <div className="unit-summary-row">
            <div>
              <h3 style={{ marginBottom: 4 }}>{activeUnit?.title}</h3>
              <p className="field-hint" style={{ maxWidth: 520 }}>
                {activeUnit?.description}
              </p>
            </div>
            <div className="unit-summary-actions">
              <span className="price price-lg">
                {activeUnit?.price_from}–{activeUnit?.price_to} €<span className="price-label"> / ночь</span>
              </span>
              <button
                className={`btn ${selectedUnit === activeUnit?.unit_uuid ? 'btn-brass' : 'btn-secondary'}`}
                onClick={() => activeUnit && pickUnit(activeUnit)}
              >
                Забронировать
              </button>
            </div>
          </div>

          {categories.length > 1 && (
            <div className="unit-dots">
              {categories.map((c, i) => (
                <button
                  key={c.unit_uuid}
                  className={`unit-dot${i === unitIndex ? ' active' : ''}`}
                  onClick={() => setUnitIndex(i)}
                  aria-label={c.title}
                />
              ))}
            </div>
          )}

          <hr className="rule" />
        </>
      )}

      {/* ---------- Reviews + booking form ---------- */}
      <div className="two-col">
        <div>
          <h2>Отзывы</h2>
          <p className="field-hint" style={{ marginTop: -8, marginBottom: 20 }}>
            Оставить отзыв можно только после успешного проживания — в течение 3 дней после выезда.
          </p>

          {listing.reviews?.length ? (
            <div className="row-list">
              {listing.reviews.map((r) => (
                <div className="review-card" key={r.uuid}>
                  <div className="review-head">
                    <span className="avatar-circle">{initials(r.user)}</span>
                    <div className="review-head-meta">
                      <div className="row-title">{r.user}</div>
                      <div className="field-hint">{new Date(r.created_at).toLocaleDateString('ru-RU')}</div>
                    </div>
                    <div className="review-rating">
                      <StarIcon />
                      <span>{r.rating}/10</span>
                    </div>
                  </div>
                  <p className="review-text">{r.comment}</p>
                  <div className="review-foot">
                    <button className="review-vote" aria-label="Полезно">
                      <ThumbUpIcon />
                    </button>
                    <button className="review-vote" aria-label="Не полезно">
                      <ThumbDownIcon />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="field-hint">Пока нет отзывов.</p>
          )}
        </div>

        <div className="card card-pad side-card" id="book">
          <h3>Забронировать</h3>
          {activeUnit && (
            <p className="field-hint" style={{ marginTop: -8 }}>
              Номер: <strong>{categories.find((c) => c.unit_uuid === selectedUnit)?.title || activeUnit.title}</strong>
            </p>
          )}
          <ErrorBanner message={bookingError} />
          <SuccessBanner message={bookingSuccess} />
          <form onSubmit={submitBooking}>
            {categories.length > 1 && (
              <div className="field">
                <label>Номер</label>
                <select value={selectedUnit} onChange={(e) => setSelectedUnit(e.target.value)}>
                  {categories.map((c) => (
                    <option key={c.unit_uuid} value={c.unit_uuid}>
                      {c.title} — {c.price_from}–{c.price_to} €/ночь
                    </option>
                  ))}
                </select>
              </div>
            )}
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
