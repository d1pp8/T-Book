import { useState } from 'react';

export function Spinner() {
  return (
    <div className="spinner-wrap">
      <div className="spinner" />
    </div>
  );
}

export function ErrorBanner({ message }) {
  if (!message) return null;
  return <div className="banner banner-error">{message}</div>;
}

export function SuccessBanner({ message }) {
  if (!message) return null;
  return <div className="banner banner-success">{message}</div>;
}

export function Empty({ title, hint }) {
  return (
    <div className="empty">
      <h3>{title}</h3>
      {hint && <p>{hint}</p>}
    </div>
  );
}

export function StatusStamp({ status, labels }) {
  const label = labels?.[status] || status;
  return <span className={`stamp stamp-${status}`}>{label}</span>;
}

export function Pagination({ page, hasNext, hasPrev, onChange }) {
  if (!hasNext && !hasPrev) return null;
  return (
    <div className="pagination">
      <button className="btn btn-secondary btn-sm" disabled={!hasPrev} onClick={() => onChange(page - 1)}>
        ← Назад
      </button>
      <span className="field-hint" style={{ alignSelf: 'center' }}>
        стр. {page}
      </span>
      <button className="btn btn-secondary btn-sm" disabled={!hasNext} onClick={() => onChange(page + 1)}>
        Вперёд →
      </button>
    </div>
  );
}

export function Modal({ title, onClose, children }) {
  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h3>{title}</h3>
        {children}
      </div>
    </div>
  );
}

export function ConfirmButton({ label, confirmLabel = 'Точно?', onConfirm, className = 'btn btn-secondary btn-sm' }) {
  const [confirming, setConfirming] = useState(false);
  if (confirming) {
    return (
      <span className="btn-row">
        <button className="btn btn-danger btn-sm" onClick={() => onConfirm()}>
          {confirmLabel}
        </button>
        <button className="btn btn-secondary btn-sm" onClick={() => setConfirming(false)}>
          Отмена
        </button>
      </span>
    );
  }
  return (
    <button className={className} onClick={() => setConfirming(true)}>
      {label}
    </button>
  );
}
