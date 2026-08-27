import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import { apiErrorMessage } from '../api/client';
import { ErrorBanner } from '../components/Common';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setError('');
    setBusy(true);
    try {
      await login(form.email, form.password);
      navigate(location.state?.from?.pathname || '/', { replace: true });
    } catch (err) {
      setError(apiErrorMessage(err, 'Incorrect email or password.'));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '0 auto' }}>
      <p className="eyebrow">Log In</p>
      <h1>Welcome back</h1>
      <p className="subtitle">Log in to book and manage properties.</p>
      <div className="card card-pad">
        <ErrorBanner message={error} />
        <form onSubmit={submit}>
          <div className="field">
            <label>Email</label>
            <input
              type="email"
              required
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
          </div>
          <div className="field">
            <label>Password</label>
            <input
              type="password"
              required
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />
          </div>
          <button className="btn" style={{ width: '100%' }} disabled={busy}>
            {busy ? 'Logging in…' : 'Log In'}
          </button>
        </form>
      </div>
      <p className="field-hint" style={{ marginTop: 16 }}>
        Don't have an account? <Link to="/register">Sign up</Link>
      </p>
    </div>
  );
}
