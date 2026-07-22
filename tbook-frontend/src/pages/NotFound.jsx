import { Link } from 'react-router-dom';

export default function NotFound() {
  return (
    <div className="empty">
      <h3>Страница не найдена</h3>
      <p>
        <Link to="/">Вернуться в каталог</Link>
      </p>
    </div>
  );
}
