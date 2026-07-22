import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { listingsApi } from '../api/endpoints';
import { apiErrorMessage } from '../api/client';
import { Spinner, Empty, ErrorBanner, Pagination } from '../components/Common';
import { PROPERTY_TYPES, labelFor } from '../constants';

const emptySearch = { check_in: '', check_out: '', adults: '', children: '' };

export default function Home() {
  const [search, setSearch] = useState(emptySearch);
  const [appliedSearch, setAppliedSearch] = useState(emptySearch);
  const [page, setPage] = useState(1);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError('');
    const params = { page };
    Object.entries(appliedSearch).forEach(([k, v]) => {
      if (v) params[k] = v;
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

  const submitSearch = (e) => {
    e.preventDefault();
    setPage(1);
    setAppliedSearch(search);
  };

  return (
    <div>
      <p className="eyebrow">Каталог</p>
      <h1>Найдите жильё для следующей поездки</h1>
      <p className="subtitle">Отели, апартаменты и дома, доступные для бронирования прямо сейчас.</p>

      <form className="card card-pad" onSubmit={submitSearch} style={{ marginBottom: 32 }}>
        <div className="field-row">
          <div className="field">
            <label>Заезд</label>
            <input type="date" value={search.check_in} onChange={(e) => setSearch({ ...search, check_in: e.target.value })} />
          </div>
          <div className="field">
            <label>Выезд</label>
            <input type="date" value={search.check_out} onChange={(e) => setSearch({ ...search, check_out: e.target.value })} />
          </div>
        </div>
        <div className="field-row">
          <div className="field">
            <label>Взрослые</label>
            <input type="number" min="0" value={search.adults} onChange={(e) => setSearch({ ...search, adults: e.target.value })} />
          </div>
          <div className="field">
            <label>Дети</label>
            <input type="number" min="0" value={search.children} onChange={(e) => setSearch({ ...search, children: e.target.value })} />
          </div>
        </div>
        <button className="btn btn-brass">Искать</button>
      </form>

      <ErrorBanner message={error} />
      {loading && <Spinner />}

      {!loading && data && data.results.length === 0 && (
        <Empty title="Ничего не найдено" hint="Попробуйте изменить даты или количество гостей." />
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
