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
      setError(apiErrorMessage(err, 'Failed to sign up.'));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div style={{ maxWidth: 440, margin: '0 auto' }}>
      <p className="eyebrow">Sign Up</p>
      <h1>New account</h1>
      <p className="subtitle">
        New accounts get the "Guest" role. To list properties, ask an administrator to grant you
        the "Owner" role.
      </p>
      <div className="card card-pad">
        <ErrorBanner message={error} />
        <form onSubmit={submit}>
          <div className="field-row">
            <div className="field">
              <label>First name</label>
              <input value={form.first_name} onChange={set('first_name')} />
            </div>
            <div className="field">
              <label>Last name</label>
              <input value={form.last_name} onChange={set('last_name')} />
            </div>
          </div>
          <div className="field">
            <label>Email</label>
            <input type="email" required value={form.email} onChange={set('email')} />
          </div>
          <div className="field-row">
            <div className="field">
              <label>Password</label>
              <input type="password" required value={form.password} onChange={set('password')} />
            </div>
            <div className="field">
              <label>Confirm password</label>
              <input type="password" required value={form.password2} onChange={set('password2')} />
            </div>
          </div>
          <button className="btn" style={{ width: '100%' }} disabled={busy}>
            {busy ? 'Creating…' : 'Sign Up'}
          </button>
        </form>
      </div>
      <p className="field-hint" style={{ marginTop: 16 }}>
        Already have an account? <Link to="/login">Log In</Link>
      </p>
    </div>
  );
}
