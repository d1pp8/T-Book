import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import { apiErrorMessage } from '../api/client';
import { ErrorBanner } from '../components/Common';

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    email: '',
    password: '',
    password2: '',
    first_name: '',
    last_name: '',
  });
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const set = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setError('');
    setBusy(true);
    try {
      await register(form);
      navigate('/', { replace: true });
    } catch (err) {
      setError(apiErrorMessage(err, 'Не удалось зарегистрироваться.'));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div style={{ maxWidth: 440, margin: '0 auto' }}>
      <p className="eyebrow">Регистрация</p>
      <h1>Новый аккаунт</h1>
      <p className="subtitle">
        Новые аккаунты получают роль «Гость». Чтобы размещать объекты, попросите администратора выдать роль
        «Владелец».
      </p>
      <div className="card card-pad">
        <ErrorBanner message={error} />
        <form onSubmit={submit}>
          <div className="field-row">
            <div className="field">
              <label>Имя</label>
              <input value={form.first_name} onChange={set('first_name')} />
            </div>
            <div className="field">
              <label>Фамилия</label>
              <input value={form.last_name} onChange={set('last_name')} />
            </div>
          </div>
          <div className="field">
            <label>Email</label>
            <input type="email" required value={form.email} onChange={set('email')} />
          </div>
          <div className="field-row">
            <div className="field">
              <label>Пароль</label>
              <input type="password" required value={form.password} onChange={set('password')} />
            </div>
            <div className="field">
              <label>Повторите пароль</label>
              <input type="password" required value={form.password2} onChange={set('password2')} />
            </div>
          </div>
          <button className="btn" style={{ width: '100%' }} disabled={busy}>
            {busy ? 'Создаём…' : 'Зарегистрироваться'}
          </button>
        </form>
      </div>
      <p className="field-hint" style={{ marginTop: 16 }}>
        Уже есть аккаунт? <Link to="/login">Войти</Link>
      </p>
    </div>
  );
}
