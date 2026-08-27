import { useEffect, useState } from 'react';
import { ownerBookingApi } from '../api/endpoints';
import { apiErrorMessage } from '../api/client';
import { Spinner, Empty, ErrorBanner, SuccessBanner, StatusStamp, ConfirmButton } from '../components/Common';
import BookingDetailModal from '../components/BookingDetail';
import { BOOKING_STATUS_LABELS } from '../constants';

const TABS = [
  { key: 'active', label: 'Active', loader: ownerBookingApi.active },
  { key: 'pending', label: 'Pending', loader: ownerBookingApi.pending },
  { key: 'confirmed', label: 'Confirmed', loader: ownerBookingApi.confirmed },
  { key: 'completed', label: 'Completed', loader: ownerBookingApi.completed },
  { key: 'cancelled', label: 'Cancelled/Rejected', loader: ownerBookingApi.cancelledRejected },
  { key: 'all', label: 'All', loader: ownerBookingApi.all },
];

export default function OwnerBookings() {
  const [tab, setTab] = useState('pending');
  const [items, setItems] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [busyUuid, setBusyUuid] = useState('');
  const [detailTarget, setDetailTarget] = useState(null);

  const load = () => {
    setLoading(true);
    setError('');
    const tabDef = TABS.find((t) => t.key === tab);
    tabDef
      .loader()
      .then(({ data }) => setItems(data.results ?? data))
      .catch((err) => setError(apiErrorMessage(err, 'Failed to load bookings.')))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tab]);

  const act = async (action, uuid, doneMsg) => {
    setBusyUuid(uuid);
    setNotice('');
    setError('');
    try {
      await action(uuid);
      setNotice(doneMsg);
      load();
    } catch (err) {
      setError(apiErrorMessage(err, 'Action failed.'));
    } finally {
      setBusyUuid('');
    }
  };

  return (
    <div>
      <p className="eyebrow">Owner Dashboard</p>
      <h1>Booking Requests</h1>

      <div className="tabs">
        {TABS.map((t) => (
          <button key={t.key} className={`tab${tab === t.key ? ' active' : ''}`} onClick={() => setTab(t.key)}>
            {t.label}
          </button>
        ))}
      </div>

      <ErrorBanner message={error} />
      <SuccessBanner message={notice} />
      {loading && <Spinner />}

      {!loading && items && items.length === 0 && (
        <Empty title="Nothing here yet" hint="Booking requests will appear here." />
      )}

      {!loading && items && items.length > 0 && (
        <div className="row-list">
          {items.map((b) => (
            <div className="row-item" key={b.uuid}>
              <div className="row-main">
                <span className="row-title">{b.property_title}{b.unit_title ? ` — ${b.unit_title}` : ''}</span>
                <span className="row-meta">
                  {b.user?.full_name || b.user?.email} · {b.check_in} → {b.check_out} · {b.number_of_guests} guests · {b.total_price} €
                </span>
              </div>
              <div className="row-actions">
                <StatusStamp status={b.status} labels={BOOKING_STATUS_LABELS} />
                <button className="btn btn-secondary btn-sm" onClick={() => setDetailTarget(b.uuid)}>
                  Details
                </button>
                {b.status === 'pending' && (
                  <>
                    <button className="btn btn-brass btn-sm" disabled={busyUuid === b.uuid} onClick={() => act(ownerBookingApi.confirm, b.uuid, 'Booking confirmed.')}>
                      Confirm
                    </button>
                    <ConfirmButton label="Reject" confirmLabel="Really reject?" onConfirm={() => act(ownerBookingApi.reject, b.uuid, 'Booking rejected.')} />
                  </>
                )}
                {b.status === 'confirmed' && (
                  <button className="btn btn-secondary btn-sm" disabled={busyUuid === b.uuid} onClick={() => act(ownerBookingApi.complete, b.uuid, 'Booking completed.')}>
                    Complete
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {detailTarget && (
        <BookingDetailModal
          title="Request Details"
          loadDetail={() => ownerBookingApi.detail(detailTarget)}
          onClose={() => setDetailTarget(null)}
          isOwnerView
        />
      )}
    </div>
  );
}
