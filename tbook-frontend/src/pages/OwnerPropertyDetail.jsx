import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { propertyApi, unitApi, catalogApi, propertyImageApi } from '../api/endpoints';
import { apiErrorMessage } from '../api/client';
import { Spinner, Empty, ErrorBanner, SuccessBanner, StatusStamp, ConfirmButton } from '../components/Common';
import { PROPERTY_TYPES, PROPERTY_STATUSES, UNIT_STATUSES, labelFor } from '../constants';

const emptyUnit = {
  title: '',
  description: '',
  status: 'available',
  price_per_night: '',
  area: '',
  bedrooms: '',
  bathrooms: '',
  max_guests: '',
  room_number: '',
  amenities: [],
};

export default function OwnerPropertyDetail() {
  const { propertyUuid } = useParams();
  const navigate = useNavigate();
  const [property, setProperty] = useState(null);
  const [units, setUnits] = useState(null);
  const [amenities, setAmenities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  const [form, setForm] = useState(null);
  const [saving, setSaving] = useState(false);

  const [showUnitForm, setShowUnitForm] = useState(false);
  const [unitForm, setUnitForm] = useState(emptyUnit);
  const [unitError, setUnitError] = useState('');
  const [unitBusy, setUnitBusy] = useState(false);

  const fileInput = useRef(null);
  const [uploading, setUploading] = useState(false);

  const load = () => {
    setLoading(true);
    Promise.all([propertyApi.detail(propertyUuid), unitApi.list(propertyUuid)])
      .then(([p, u]) => {
        setProperty(p.data);
        setForm({
          status: p.data.status,
          title: p.data.title,
          description: p.data.description,
          country: p.data.country,
          city: p.data.city,
          street: p.data.street,
          house_number: p.data.house_number,
          postal_code: p.data.postal_code || '',
          floor: p.data.floor ?? '',
          amenities: (p.data.amenities || []).map((a) => a.uuid),
        });
        setUnits(u.data.results ?? u.data);
      })
      .catch((err) => setError(apiErrorMessage(err, 'Не удалось загрузить объект.')))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
    catalogApi.amenities().then(({ data }) => setAmenities(data.results ?? data)).catch(() => {});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [propertyUuid]);

  const toggleAmenity = (uuid) => {
    setForm((f) => ({
      ...f,
      amenities: f.amenities.includes(uuid) ? f.amenities.filter((a) => a !== uuid) : [...f.amenities, uuid],
    }));
  };

  const saveProperty = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    try {
      const payload = { ...form, floor: form.floor === '' ? null : Number(form.floor) };
      const { data } = await propertyApi.update(propertyUuid, payload);
      setProperty(data);
      setNotice('Изменения сохранены.');
    } catch (err) {
      setError(apiErrorMessage(err, 'Не удалось сохранить изменения.'));
    } finally {
      setSaving(false);
    }
  };

  const deleteProperty = async () => {
    try {
      await propertyApi.remove(propertyUuid);
      navigate('/owner/properties', { replace: true });
    } catch (err) {
      setError(apiErrorMessage(err, 'Не удалось удалить объект (возможно, есть активные бронирования).'));
    }
  };

  const uploadImages = async (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;
    setUploading(true);
    setError('');
    try {
      await propertyImageApi.upload(propertyUuid, files);
      load();
    } catch (err) {
      setError(apiErrorMessage(err, 'Не удалось загрузить изображения.'));
    } finally {
      setUploading(false);
      if (fileInput.current) fileInput.current.value = '';
    }
  };

  const deleteImage = async (imageUuid) => {
    try {
      await propertyImageApi.remove(propertyUuid, imageUuid);
      load();
    } catch (err) {
      setError(apiErrorMessage(err, 'Не удалось удалить изображение.'));
    }
  };

  const setCoverImage = async (imageUuid) => {
    try {
      await propertyImageApi.setCover(propertyUuid, imageUuid);
      load();
    } catch (err) {
      setError(apiErrorMessage(err, 'Не удалось выбрать обложку.'));
    }
  };

  const toggleUnitAmenity = (uuid) => {
    setUnitForm((f) => ({
      ...f,
      amenities: f.amenities.includes(uuid) ? f.amenities.filter((a) => a !== uuid) : [...f.amenities, uuid],
    }));
  };

  const createUnit = async (e) => {
    e.preventDefault();
    setUnitBusy(true);
    setUnitError('');
    try {
      const payload = {
        ...unitForm,
        price_per_night: Number(unitForm.price_per_night),
        area: Number(unitForm.area),
        bedrooms: Number(unitForm.bedrooms),
        bathrooms: Number(unitForm.bathrooms),
        max_guests: Number(unitForm.max_guests),
        beds: [],
      };
      await unitApi.create(propertyUuid, payload);
      setUnitForm(emptyUnit);
      setShowUnitForm(false);
      setNotice('Юнит создан. Кровати и фото можно добавить на странице юнита.');
      load();
    } catch (err) {
      setUnitError(apiErrorMessage(err, 'Не удалось создать юнит.'));
    } finally {
      setUnitBusy(false);
    }
  };

  if (loading) return <Spinner />;
  if (!property || !form) return <ErrorBanner message={error || 'Объект не найден.'} />;

  return (
    <div>
      <p className="eyebrow">{labelFor(PROPERTY_TYPES, property.type)}</p>
      <h1>{property.title}</h1>
      <SuccessBanner message={notice} />
      <ErrorBanner message={error} />

      <div className="two-col">
        <div>
          <h3>Изображения</h3>
          <div className="gallery" style={{ marginBottom: 12 }}>
            {property.images?.map((img) => (
              <div className="gallery-item" key={img.uuid}>
                <img src={img.image} alt="" />
                {img.is_cover && <span className="cover-badge">Обложка</span>}
                <div className="gallery-actions">
                  {!img.is_cover && <button onClick={() => setCoverImage(img.uuid)}>Сделать обложкой</button>}
                  <button onClick={() => deleteImage(img.uuid)}>Удалить</button>
                </div>
              </div>
            ))}
          </div>
          <input ref={fileInput} type="file" multiple accept="image/jpeg,image/png,image/webp" onChange={uploadImages} disabled={uploading} />
          {uploading && <p className="field-hint">Загружаем…</p>}

          <hr className="rule" />

          <h3>Информация об объекте</h3>
          <form onSubmit={saveProperty}>
            <div className="field">
              <label>Название</label>
              <input required value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
            </div>
            <div className="field">
              <label>Описание</label>
              <textarea rows={3} required value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
            </div>
            <div className="field">
              <label>Статус</label>
              <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                {PROPERTY_STATUSES.map((s) => (
                  <option key={s.value} value={s.value}>{s.label}</option>
                ))}
              </select>
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
            <div className="btn-row">
              <button className="btn" disabled={saving}>
                {saving ? 'Сохраняем…' : 'Сохранить изменения'}
              </button>
              <ConfirmButton label="Удалить объект" confirmLabel="Точно удалить?" onConfirm={deleteProperty} className="btn btn-danger" />
            </div>
          </form>
        </div>

        <div>
          <h3>Юниты / номера</h3>
          <button className="btn btn-secondary btn-sm" style={{ marginBottom: 16 }} onClick={() => setShowUnitForm((v) => !v)}>
            {showUnitForm ? 'Скрыть форму' : '+ Новый юнит'}
          </button>

          {showUnitForm && (
            <div className="card card-pad" style={{ marginBottom: 20 }}>
              <ErrorBanner message={unitError} />
              <form onSubmit={createUnit}>
                <div className="field">
                  <label>Название</label>
                  <input value={unitForm.title} onChange={(e) => setUnitForm({ ...unitForm, title: e.target.value })} />
                </div>
                <div className="field">
                  <label>Описание</label>
                  <textarea rows={2} value={unitForm.description} onChange={(e) => setUnitForm({ ...unitForm, description: e.target.value })} />
                </div>
                <div className="field">
                  <label>Статус</label>
                  <select value={unitForm.status} onChange={(e) => setUnitForm({ ...unitForm, status: e.target.value })}>
                    {UNIT_STATUSES.map((s) => (
                      <option key={s.value} value={s.value}>{s.label}</option>
                    ))}
                  </select>
                </div>
                <div className="field-row">
                  <div className="field">
                    <label>Цена/ночь</label>
                    <input type="number" step="0.01" required value={unitForm.price_per_night} onChange={(e) => setUnitForm({ ...unitForm, price_per_night: e.target.value })} />
                  </div>
                  <div className="field">
                    <label>Площадь, м²</label>
                    <input type="number" required value={unitForm.area} onChange={(e) => setUnitForm({ ...unitForm, area: e.target.value })} />
                  </div>
                </div>
                <div className="field-row">
                  <div className="field">
                    <label>Спальни</label>
                    <input type="number" required value={unitForm.bedrooms} onChange={(e) => setUnitForm({ ...unitForm, bedrooms: e.target.value })} />
                  </div>
                  <div className="field">
                    <label>Ванные</label>
                    <input type="number" required value={unitForm.bathrooms} onChange={(e) => setUnitForm({ ...unitForm, bathrooms: e.target.value })} />
                  </div>
                </div>
                <div className="field-row">
                  <div className="field">
                    <label>Гостей макс.</label>
                    <input type="number" required value={unitForm.max_guests} onChange={(e) => setUnitForm({ ...unitForm, max_guests: e.target.value })} />
                  </div>
                  <div className="field">
                    <label>№ комнаты</label>
                    <input value={unitForm.room_number} onChange={(e) => setUnitForm({ ...unitForm, room_number: e.target.value })} />
                  </div>
                </div>
                {amenities.length > 0 && (
                  <div className="field">
                    <label>Удобства</label>
                    <div className="checkbox-grid">
                      {amenities.map((a) => (
                        <span key={a.uuid} className={`chip${unitForm.amenities.includes(a.uuid) ? ' selected' : ''}`} onClick={() => toggleUnitAmenity(a.uuid)}>
                          {a.title}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                <button className="btn btn-brass" disabled={unitBusy}>
                  {unitBusy ? 'Создаём…' : 'Создать юнит'}
                </button>
              </form>
            </div>
          )}

          {units && units.length === 0 && <Empty title="Юнитов пока нет" hint="Добавьте первый номер или юнит." />}

          {units && units.length > 0 && (
            <div className="row-list">
              {units.map((u) => (
                <Link key={u.uuid} to={`/owner/properties/${propertyUuid}/units/${u.uuid}`} className="row-item" style={{ textDecoration: 'none', color: 'inherit' }}>
                  <div className="row-main">
                    <span className="row-title">{u.title || 'Без названия'}</span>
                    <span className="row-meta">{u.price_per_night} €/ночь · до {u.max_guests} гостей · {u.area} м²</span>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
