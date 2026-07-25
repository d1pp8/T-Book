import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { listingsApi } from '../api/endpoints';
import { apiErrorMessage } from '../api/client';
import { Spinner, Empty, ErrorBanner, Pagination } from '../components/Common';
import { PROPERTY_TYPES, SORT_OPTIONS, labelFor } from '../constants';

const emptySearch = {
  // availability
  check_in: '',
  check_out: '',
  adults: '',
  children: '',
  // catalog filters
  search: '',
  type: '',
  city: '',
  min_price: '',
  max_price: '',
  bedrooms: '',
  bathrooms: '',
  min_rating: '',
  ordering: '',
};

export default function Home() {
  const [search, setSearch] = useState(emptySearch);
  const [appliedSearch, setAppliedSearch] = useState(emptySearch);
  const [page, setPage] = useState(1);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showMore, setShowMore] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError('');
    const params = { page };
    Object.entries(appliedSearch).forEach(([k, v]) => {
      if (v !== '' && v != null) params[k] = v;
    });
    listingsApi
      .list(params)
      .then(({ data }) => {
        if (!cancelled) setData(data);
      })
      .catch((err) => {
        if (!cancelled) setError(apiErrorMessage(err, 'Не удалось загрузить каталог.'));
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [appliedSearch, page]);

  const set = (field) => (e) => setSearch({ ...search, [field]: e.target.value });

  const submitSearch = (e) => {
    e.preventDefault();
    setPage(1);
    setAppliedSearch(search);
  };

  const resetSearch = () => {
    setSearch(emptySearch);
    setPage(1);
    setAppliedSearch(emptySearch);
  };

  const activeExtraCount = ['search', 'type', 'city', 'min_price', 'max_price', 'bedrooms', 'bathrooms', 'min_rating', 'ordering'].filter(
    (k) => appliedSearch[k]
  ).length;

  return (
    <div>
      <p className="eyebrow">Каталог</p>
      <h1>Найдите жильё для следующей поездки</h1>
      <p className="subtitle">Отели, апартаменты и дома, доступные для бронирования прямо сейчас.</p>

      <form className="card card-pad" onSubmit={submitSearch} style={{ marginBottom: 32 }}>
        <div className="field-row">
          <div className="field">
            <label>Заезд</label>
            <input type="date" value={search.check_in} onChange={set('check_in')} />
          </div>
          <div className="field">
            <label>Выезд</label>
            <input type="date" min={search.check_in || undefined} value={search.check_out} onChange={set('check_out')} />
          </div>
        </div>
        <div className="field-row">
          <div className="field">
            <label>Взрослые</label>
            <input type="number" min="0" value={search.adults} onChange={set('adults')} />
          </div>
          <div className="field">
            <label>Дети</label>
            <input type="number" min="0" value={search.children} onChange={set('children')} />
          </div>
        </div>
        <div className="field">
          <label>Поиск по названию/описанию</label>
          <input value={search.search} onChange={set('search')} placeholder="Например: вилла у моря" />
        </div>

        <button
          type="button"
          className="field-hint"
          style={{ background: 'none', border: 'none', padding: 0, cursor: 'pointer', textAlign: 'left', marginBottom: 12 }}
          onClick={() => setShowMore((v) => !v)}
        >
          {showMore ? '▲ Скрыть дополнительные фильтры' : `▼ Дополнительные фильтры${activeExtraCount ? ` (${activeExtraCount})` : ''}`}
        </button>

        {showMore && (
          <>
            <div className="field-row">
              <div className="field">
                <label>Тип жилья</label>
                <select value={search.type} onChange={set('type')}>
                  <option value="">Любой</option>
                  {PROPERTY_TYPES.map((t) => (
                    <option key={t.value} value={t.value}>{t.label}</option>
                  ))}
                </select>
              </div>
              <div className="field">
                <label>Город</label>
                <input value={search.city} onChange={set('city')} placeholder="Например: Берлин" />
              </div>
            </div>
            <div className="field-row">
              <div className="field">
                <label>Цена от, €/ночь</label>
                <input type="number" min="0" value={search.min_price} onChange={set('min_price')} />
              </div>
              <div className="field">
                <label>Цена до, €/ночь</label>
                <input type="number" min="0" value={search.max_price} onChange={set('max_price')} />
              </div>
            </div>
            <div className="field-row">
              <div className="field">
                <label>Спален от</label>
                <input type="number" min="0" value={search.bedrooms} onChange={set('bedrooms')} />
              </div>
              <div className="field">
                <label>Ванных от</label>
                <input type="number" min="0" value={search.bathrooms} onChange={set('bathrooms')} />
              </div>
            </div>
            <div className="field-row">
              <div className="field">
                <label>Рейтинг от</label>
                <input type="number" min="0" max="10" step="0.1" value={search.min_rating} onChange={set('min_rating')} />
              </div>
              <div className="field">
                <label>Сортировка</label>
                <select value={search.ordering} onChange={set('ordering')}>
                  {SORT_OPTIONS.map((o) => (
                    <option key={o.value} value={o.value}>{o.label}</option>
                  ))}
                </select>
              </div>
            </div>
          </>
        )}

        <div className="btn-row">
          <button className="btn btn-brass">Искать</button>
          <button type="button" className="btn btn-secondary" onClick={resetSearch}>
            Сбросить
          </button>
        </div>
      </form>

      <ErrorBanner message={error} />
      {loading && <Spinner />}

      {!loading && data && data.results.length === 0 && (
        <Empty title="Ничего не найдено" hint="Попробуйте изменить даты, фильтры или количество гостей." />
      )}

      {!loading && data && data.results.length > 0 && (
        <>
          <div className="grid">
            {data.results.map((item) => (
              <Link to={`/listings/${item.uuid}`} key={item.uuid} className="listing-card">
                <div
                  className="listing-card-image"
                  style={item.cover_image ? { backgroundImage: `url(${item.cover_image})` } : undefined}
                >
                  <span className="listing-card-type">{labelFor(PROPERTY_TYPES, item.type)}</span>
                </div>
                <div className="listing-card-body">
                  <div className="listing-card-title">{item.title}</div>
                  <div className="listing-card-loc">{item.city}, {item.country}</div>
                  <div className="listing-card-foot">
                    <div>
                      <div className="price">от {item.price_from} €</div>
                      <div className="price-label">за ночь</div>
                    </div>
                    <div className="rating">★ {item.rating} ({item.review_count})</div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
          <Pagination page={page} hasNext={!!data.next} hasPrev={!!data.previous} onChange={setPage} />
        </>
      )}
    </div>
  );
}
