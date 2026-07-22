import { useState } from 'react';
import { useAuth } from '../AuthContext';
import { authApi } from '../api/endpoints';
import { apiErrorMessage } from '../api/client';
import { ErrorBanner, SuccessBanner } from '../components/Common';
import { ROLE_LABELS } from '../constants';

export default function Profile() {
  const { user, refreshUser } = useAuth();
  const [form, setForm] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    phone: user?.phone || '',
  });
  const [saveMsg, setSaveMsg] = useState('');
  const [saveErr, setSaveErr] = useState('');
  const [busy, setBusy] = useState(false);

  const [pwd, setPwd] = useState({ old_password: '', new_password: '', new_password2: '' });
  const [pwdMsg, setPwdMsg] = useState('');
  const [pwdErr, setPwdErr] = useState('');
  const [pwdBusy, setPwdBusy] = useState(false);

  if (!user) return null;

  const saveProfile = async (e) => {
    e.preventDefault();
    setSaveErr('');
    setSaveMsg('');
    setBusy(true);
    try {
      await authApi.updateProfile(form);
      await refreshUser();
      setSaveMsg('Профиль обновлён.');
    } catch (err) {
      setSaveErr(apiErrorMessage(err));
    } finally {
      setBusy(false);
    }
  };

  const changePassword = async (e) => {
    e.preventDefault();
    setPwdErr('');
    setPwdMsg('');
    setPwdBusy(true);
    try {
      await authApi.changePassword(pwd);
      setPwdMsg('Пароль изменён.');
      setPwd({ old_password: '', new_password: '', new_password2: '' });
    } catch (err) {
      setPwdErr(apiErrorMessage(err));
    } finally {
      setPwdBusy(false);
    }
  };

  return (
    <div style={{ maxWidth: 520 }}>
      <p className="eyebrow">Профиль</p>
      <h1>{user.email}</h1>
      <p className="subtitle">Роль: {ROLE_LABELS[user.role] || user.role}</p>

      <div className="card card-pad" style={{ marginBottom: 24 }}>
        <h3>Личные данные</h3>
        <ErrorBanner message={saveErr} />
        <SuccessBanner message={saveMsg} />
        <form onSubmit={saveProfile}>
          <div className="field-row">
            <div className="field">
              <label>Имя</label>
              <input value={form.first_name} onChange={(e) => setForm({ ...form, first_name: e.target.value })} />
            </div>
            <div className="field">
              <label>Фамилия</label>
              <input value={form.last_name} onChange={(e) => setForm({ ...form, last_name: e.target.value })} />
            </div>
          </div>
          <div className="field">
            <label>Телефон</label>
            <input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
          </div>
          <button className="btn" disabled={busy}>
            {busy ? 'Сохраняем…' : 'Сохранить'}
          </button>
        </form>
      </div>

      <div className="card card-pad">
        <h3>Смена пароля</h3>
        <ErrorBanner message={pwdErr} />
        <SuccessBanner message={pwdMsg} />
        <form onSubmit={changePassword}>
          <div className="field">
            <label>Текущий пароль</label>
            <input
              type="password"
              required
              value={pwd.old_password}
              onChange={(e) => setPwd({ ...pwd, old_password: e.target.value })}
            />
          </div>
          <div className="field-row">
            <div className="field">
              <label>Новый пароль</label>
              <input
                type="password"
                required
                value={pwd.new_password}
                onChange={(e) => setPwd({ ...pwd, new_password: e.target.value })}
              />
            </div>
            <div className="field">
              <label>Повторите новый пароль</label>
              <input
                type="password"
                required
                value={pwd.new_password2}
                onChange={(e) => setPwd({ ...pwd, new_password2: e.target.value })}
              />
            </div>
          </div>
          <button className="btn btn-secondary" disabled={pwdBusy}>
            {pwdBusy ? 'Меняем…' : 'Изменить пароль'}
          </button>
        </form>
      </div>
    </div>
  );
}
