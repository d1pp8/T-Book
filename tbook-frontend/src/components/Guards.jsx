import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import { Spinner } from './Common';

export function RequireAuth({ children }) {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();
  if (loading) return <Spinner />;
  if (!isAuthenticated) return <Navigate to="/login" state={{ from: location }} replace />;
  return children;
}

export function RequireOwner({ children }) {
  const { isOwner, loading, isAuthenticated } = useAuth();
  const location = useLocation();
  if (loading) return <Spinner />;
  if (!isAuthenticated) return <Navigate to="/login" state={{ from: location }} replace />;
  if (!isOwner) {
    return (
      <div className="empty">
        <h3>Доступно только владельцам</h3>
        <p>Эта страница открыта пользователям с ролью «Владелец» или «Администратор».</p>
      </div>
    );
  }
  return children;
}
