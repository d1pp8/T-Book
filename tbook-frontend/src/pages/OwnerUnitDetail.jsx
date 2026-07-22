import { useEffect, useRef, useState } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { unitApi, catalogApi, unitImageApi } from '../api/endpoints';
import { apiErrorMessage } from '../api/client';
import { Spinner, ErrorBanner, SuccessBanner, ConfirmButton } from '../components/Common';
import { UNIT_STATUSES, BED_TYPES } from '../constants';

export default function OwnerUnitDetail() {
  const { propertyUuid, unitUuid } = useParams();
  const navigate = useNavigate();
  const [unit, setUnit] = useState(null);
  const [amenities, setAmenities] = useState([]);
  const [form, setForm] = useState(null);
  const [beds, setBeds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [saving, setSaving] = useState(false);

  const fileInput = useRef(null);
  const [uploading, setUploading] = useState(false);

  const load = () => {
    setLoading(true);
    unitApi
      .detail(propertyUuid, unitUuid)
      .then(({ data }) => {
        setUnit(data);
        setForm({
          title: data.title || '',
          description: data.description || '',
          status: data.status,
          price_per_night: data.price_per_night,
          area: data.area,
          bedrooms: data.bedrooms,
          bathrooms: data.bathrooms,
          max_guests: data.max_guests,
          room_number: data.room_number || '',
          amenities: (data.amenities || []).map((a) => (typeof a === 'string' ? a : a.uuid)),
        });
        setBeds((data.beds || []).map((b) => ({ bed_type: b.bed_type, quantity: b.quantity })));
      })
      .catch((err) => setError(apiErrorMessage(err, 'Не удалось загрузить юнит.')))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
    catalogApi.amenities().then(({ data }) => setAmenities(data.results ?? data)).catch(() => {});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [propertyUuid, unitUuid]);

  const toggleAmenity = (uuid) => {
    setForm((f) => ({
      ...f,
      amenities: f.amenities.includes(uuid) ? f.amenities.filter((a) => a !== uuid) : [...f.amenities, uuid],
    }));
  };

  const addBed = () => setBeds((b) => [...b, { bed_type: 'single', quantity: 1 }]);
  const removeBed = (idx) => setBeds((b) => b.filter((_, i) => i !== idx));
  const updateBed = (idx, field, value) => setBeds((b) => b.map((row, i) => (i === idx ? { ...row, [field]: value } : row)));

  const save = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    try {
      const payload = {
        ...form,
        price_per_night: Number(form.price_per_night),
        area: Number(form.area),
        bedrooms: Number(form.bedrooms),
        bathrooms: Number(form.bathrooms),
        max_guests: Number(form.max_guests),
        beds: beds.map((b) => ({ bed_type: b.bed_type, quantity: Number(b.quantity) })),
      };
      await unitApi.update(propertyUuid, unitUuid, payload);
      setNotice('Изменения сохранены.');
      load();
    } catch (err) {
      setError(apiErrorMessage(err, 'Не удалось сохранить изменения.'));
    } finally {
      setSaving(false);
    }
  };

  const deleteUnit = async () => {
    try {
      await unitApi.remove(propertyUuid, unitUuid);
      navigate(`/owner/properties/${propertyUuid}`, { replace: true });
    } catch (err) {
      setError(apiErrorMessage(err, 'Не удалось удалить юнит (возможно, есть активные бронирования).'));
    }
  };

  const uploadImages = async (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;
    setUploading(true);
    try {
      await unitImageApi.upload(propertyUuid, unitUuid, files);
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
      await unitImageApi.remove(propertyUuid, unitUuid, imageUuid);
      load();
    } catch (err) {
      setError(apiErrorMessage(err, 'Не удалось удалить изображение.'));
    }
  };

  const setCoverImage = async (imageUuid) => {
    try {
      await unitImageApi.setCover(propertyUuid, unitUuid, imageUuid);
      load();
    } catch (err) {
      setError(apiErrorMessage(err, 'Не удалось выбрать обложку.'));
    }
  };

  if (loading) return <Spinner />;
  if (!unit || !form) return <ErrorBanner message={error || 'Юнит не найден.'} />;

  return (
    <div>
      <Link to={`/owner/properties/${propertyUuid}`} className="field-hint">← Назад к объекту</Link>
      <p className="eyebrow" style={{ marginTop: 16 }}>Юнит</p>
      <h1>{unit.title || 'Без названия'}</h1>
      <SuccessBanner message={notice} />
      <ErrorBanner message={error} />

      <div className="two-col">
        <div>
          <h3>Изображения</h3>
          <div className="gallery" style={{ marginBottom: 12 }}>
            {unit.images?.map((img) => (
              <div className="gallery-item" key={img.uuid}>
                <img src={img.image} alt="" />
                {img.is_cover && <span className="cover-badge">Обложка</span>}
                <div className="gallery-actions">
                  {!img.is_cover && <button onClick={() => setCoverImage(img.uuid)}>Обложка</button>}
                  <button onClick={() => deleteImage(img.uuid)}>Удалить</button>
                </div>
              </div>
            ))}
          </div>
          <input ref={fileInput} type="file" multiple accept="image/jpeg,image/png,image/webp" onChange={uploadImages} disabled={uploading} />
          {uploading && <p className="field-hint">Загружаем…</p>}

          <hr className="rule" />

          <h3>Кровати</h3>
          <div className="row-list" style={{ marginBottom: 12 }}>
            {beds.map((b, idx) => (
              <div className="field-row" key={idx} style={{ alignItems: 'end' }}>
                <div className="field">
                  <label>Тип</label>
                  <select value={b.bed_type} onChange={(e) => updateBed(idx, 'bed_type', e.target.value)}>
                    {BED_TYPES.map((t) => (
                      <option key={t.value} value={t.value}>{t.label}</option>
                    ))}
                  </select>
                </div>
                <div className="field" style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
                  <input type="number" min="1" max="10" style={{ width: 80 }} value={b.quantity} onChange={(e) => updateBed(idx, 'quantity', e.target.value)} />
                  <button type="button" className="btn btn-secondary btn-sm" onClick={() => removeBed(idx)}>Удалить</button>
                </div>
              </div>
            ))}
          </div>
          <button type="button" className="btn btn-secondary btn-sm" onClick={addBed}>+ Добавить кровать</button>
        </div>

        <div>
          <h3>Параметры юнита</h3>
          <form onSubmit={save}>
            <div className="field">
              <label>Название</label>
              <input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
            </div>
            <div className="field">
              <label>Описание</label>
              <textarea rows={3} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
            </div>
            <div className="field">
              <label>Статус</label>
              <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                {UNIT_STATUSES.map((s) => (
                  <option key={s.value} value={s.value}>{s.label}</option>
                ))}
              </select>
            </div>
            <div className="field-row">
              <div className="field">
                <label>Цена/ночь</label>
                <input type="number" step="0.01" required value={form.price_per_night} onChange={(e) => setForm({ ...form, price_per_night: e.target.value })} />
              </div>
              <div className="field">
                <label>Площадь, м²</label>
                <input type="number" required value={form.area} onChange={(e) => setForm({ ...form, area: e.target.value })} />
              </div>
            </div>
            <div className="field-row">
              <div className="field">
                <label>Спальни</label>
                <input type="number" required value={form.bedrooms} onChange={(e) => setForm({ ...form, bedrooms: e.target.value })} />
              </div>
              <div className="field">
                <label>Ванные</label>
                <input type="number" required value={form.bathrooms} onChange={(e) => setForm({ ...form, bathrooms: e.target.value })} />
              </div>
            </div>
            <div className="field-row">
              <div className="field">
                <label>Гостей макс.</label>
                <input type="number" required value={form.max_guests} onChange={(e) => setForm({ ...form, max_guests: e.target.value })} />
              </div>
              <div className="field">
                <label>№ комнаты</label>
                <input value={form.room_number} onChange={(e) => setForm({ ...form, room_number: e.target.value })} />
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
              <ConfirmButton label="Удалить юнит" confirmLabel="Точно удалить?" onConfirm={deleteUnit} className="btn btn-danger" />
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
