import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { propertyApi, catalogApi } from '../api/endpoints';
import { apiErrorMessage } from '../api/client';
import { Spinner, Empty, ErrorBanner, SuccessBanner, StatusStamp } from '../components/Common';
import { PROPERTY_TYPES, PROPERTY_STATUSES, labelFor } from '../constants';

const emptyForm = {
  type: 'apartment',
  status: 'active',
  title: '',
  description: '',
  country: '',
  city: '',
  street: '',
  house_number: '',
  postal_code: '',
  floor: '',
  amenities: [],
};

export default function OwnerProperties() {
  const [properties, setProperties] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [amenities, setAmenities] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [formError, setFormError] = useState('');
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState('');

  const load = () => {
    setLoading(true);
    propertyApi
      .list()
      .then(({ data }) => setProperties(data.results ?? data))
      .catch((err) => setError(apiErrorMessage(err)))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
    catalogApi.amenities().then(({ data }) => setAmenities(data.results ?? data)).catch(() => {});
  }, []);

  const toggleAmenity = (uuid) => {
    setForm((f) => ({
      ...f,
      amenities: f.amenities.includes(uuid) ? f.amenities.filter((a) => a !== uuid) : [...f.amenities, uuid],
    }));
  };

  const submit = async (e) => {
    e.preventDefault();
    setFormError('');
    setBusy(true);
    try {
      const payload = { ...form, floor: form.floor ? Number(form.floor) : null };
      await propertyApi.create(payload);
      setShowForm(false);
      setForm(emptyForm);
      setNotice('Объект создан.');
      load();
    } catch (err) {
      setFormError(apiErrorMessage(err, 'Не удалось создать объект.'));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div>
      <p className="eyebrow">Кабинет владельца</p>
      <h1>Мои объекты</h1>
      <p className="subtitle">Отели, апартаменты и дома, которыми вы управляете.</p>

      <div className="btn-row" style={{ marginBottom: 24 }}>
        <button className="btn btn-brass" onClick={() => setShowForm((v) => !v)}>
          {showForm ? 'Скрыть форму' : '+ Новый объект'}
        </button>
      </div>

      <SuccessBanner message={notice} />

      {showForm && (
        <div className="card card-pad" style={{ marginBottom: 32 }}>
          <h3>Новый объект</h3>
          <ErrorBanner message={formError} />
          <form onSubmit={submit}>
            <div className="field-row">
              <div className="field">
                <label>Тип</label>
                <select value={form.type} onChange={(e) => setForm({ ...form, type: e.target.value })}>
                  {PROPERTY_TYPES.map((t) => (
                    <option key={t.value} value={t.value}>{t.label}</option>
                  ))}
                </select>
              </div>
              <div className="field">
                <label>Статус</label>
                <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                  {PROPERTY_STATUSES.map((s) => (
                    <option key={s.value} value={s.value}>{s.label}</option>
                  ))}
                </select>
              </div>
            </div>
            <div className="field">
              <label>Название</label>
              <input required value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
            </div>
            <div className="field">
              <label>Описание</label>
              <textarea rows={3} required value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
            </div>
            <div className="field-row">
              <div className="field">
                <label>Страна</label>
                <input required value={form.country} onChange={(e) => setForm({ ...form, country: e.target.value })} />
              </div>
              <div className="field">
                <label>Город</label>
                <input required value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} />
              </div>
            </div>
            <div className="field-row">
              <div className="field">
                <label>Улица</label>
                <input required value={form.street} onChange={(e) => setForm({ ...form, street: e.target.value })} />
              </div>
              <div className="field">
                <label>Дом</label>
                <input required value={form.house_number} onChange={(e) => setForm({ ...form, house_number: e.target.value })} />
              </div>
            </div>
            <div className="field-row">
              <div className="field">
                <label>Индекс</label>
                <input value={form.postal_code} onChange={(e) => setForm({ ...form, postal_code: e.target.value })} />
              </div>
              <div className="field">
                <label>Этаж</label>
                <input type="number" value={form.floor} onChange={(e) => setForm({ ...form, floor: e.target.value })} />
              </div>
            </div>
            {amenities.length > 0 && (
              <div className="field">
                <label>Удобства</label>
                <div className="checkbox-grid">
                  {amenities.map((a) => (
                    <span key={a.uuid} className={`chip${form.amenities.includes(a.uuid) ? ' selected' : ''}`} onClick={() => toggleAmenity(a.uuid)}>
                      {a.title}
                    </span>
                  ))}
                </div>
              </div>
            )}
            <button className="btn" disabled={busy}>
              {busy ? 'Создаём…' : 'Создать объект'}
            </button>
          </form>
        </div>
      )}

      <ErrorBanner message={error} />
      {loading && <Spinner />}

      {!loading && properties && properties.length === 0 && (
        <Empty title="Объектов пока нет" hint="Создайте первый объект, чтобы начать принимать бронирования." />
      )}

      {!loading && properties && properties.length > 0 && (
        <div className="row-list">
          {properties.map((p) => (
            <Link to={`/owner/properties/${p.uuid}`} key={p.uuid} className="row-item" style={{ textDecoration: 'none', color: 'inherit' }}>
              <div className="row-main">
                <span className="row-title">{p.title}</span>
                <span className="row-meta">{labelFor(PROPERTY_TYPES, p.type)} · {p.city}, {p.country} · ★ {p.rating}</span>
              </div>
              <StatusStamp status={p.status} labels={{ active: 'Активен', inactive: 'Неактивен', under_renovation: 'На реконструкции' }} />
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
