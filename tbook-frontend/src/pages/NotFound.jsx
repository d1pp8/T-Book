import { Link } from 'react-router-dom';

export default function NotFound() {
  return (
    <div className="empty">
      <h3>Page not found</h3>
      <p>
        <Link to="/">Back to catalog</Link>
      </p>
    </div>
  );
}
