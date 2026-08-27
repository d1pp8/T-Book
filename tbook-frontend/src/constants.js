export const PROPERTY_TYPES = [
  { value: 'hotel', label: 'Hotel' },
  { value: 'hostel', label: 'Hostel' },
  { value: 'apartment', label: 'Apartment' },
  { value: 'villa', label: 'Villa' },
  { value: 'house', label: 'House' },
];

export const PROPERTY_STATUSES = [
  { value: 'active', label: 'Active' },
  { value: 'inactive', label: 'Inactive' },
  { value: 'under_renovation', label: 'Under renovation' },
];

export const UNIT_STATUSES = [
  { value: 'available', label: 'Available' },
  { value: 'not_available', label: 'Not available' },
  { value: 'under_maintenance', label: 'Under maintenance' },
];

export const BED_TYPES = [
  { value: 'single', label: 'Single' },
  { value: 'double', label: 'Double' },
  { value: 'queen', label: 'Queen' },
  { value: 'king', label: 'King' },
  { value: 'california_king', label: 'California King' },
  { value: 'bunk_bed', label: 'Bunk bed' },
  { value: 'sofa', label: 'Sofa' },
  { value: 'pull_out_sofa', label: 'Pull-out sofa' },
  { value: 'futon', label: 'Futon' },
  { value: 'adjustable_bed', label: 'Adjustable bed' },
];

export const BOOKING_STATUS_LABELS = {
  pending: 'Awaiting confirmation',
  confirmed: 'Confirmed',
  cancelled: 'Cancelled',
  completed: 'Completed',
  rejected: 'Rejected',
};

export const SORT_OPTIONS = [
  { value: '', label: 'Default' },
  { value: 'price', label: 'Price: low to high' },
  { value: '-price', label: 'Price: high to low' },
  { value: '-created', label: 'Newest first' },
];

export const ROLE_LABELS = {
  user: 'Guest',
  owner: 'Owner',
  admin: 'Administrator',
};

export function labelFor(list, value) {
  return list.find((i) => i.value === value)?.label || value;
}
