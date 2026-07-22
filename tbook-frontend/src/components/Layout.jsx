import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import { ROLE_LABELS } from '../constants';

export default function Layout() {
  const { user, isAuthenticated, isOwner, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <>
      <nav className="nav">
        <div className="nav-inner">
          <NavLink to="/" className="brand">
            T<span className="brand-mark">·</span>Book
          </NavLink>
          <div className="nav-links">
            <NavLink to="/" end className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>
              Каталог
            </NavLink>
            {isAuthenticated && (
              <NavLink to="/bookings" className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>
                Мои брони
              </NavLink>
            )}
            {isOwner && (
              <NavLink to="/owner/properties" className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>
                Мои объекты
              </NavLink>
            )}
            {isOwner && (
              <NavLink to="/owner/bookings" className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>
                Заявки
              </NavLink>
            )}
            {isAuthenticated ? (
              <>
                <NavLink to="/profile" className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>
                  Профиль
                </NavLink>
                <span className="nav-role">{ROLE_LABELS[user?.role] || user?.role}</span>
                <button className="btn btn-secondary btn-sm" onClick={handleLogout}>
                  Выйти
                </button>
              </>
            ) : (
              <>
                <NavLink to="/login" className="nav-link">
                  Войти
                </NavLink>
                <NavLink to="/register" className="btn btn-sm">
                  Регистрация
                </NavLink>
              </>
            )}
          </div>
        </div>
      </nav>
      <main className="page container">
        <Outlet />
      </main>
    </>
  );
}
