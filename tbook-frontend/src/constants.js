export const PROPERTY_TYPES = [
  { value: 'hotel', label: 'Отель' },
  { value: 'hostel', label: 'Хостел' },
  { value: 'apartment', label: 'Апартаменты' },
  { value: 'villa', label: 'Вилла' },
  { value: 'house', label: 'Дом' },
];

export const PROPERTY_STATUSES = [
  { value: 'active', label: 'Активен' },
  { value: 'inactive', label: 'Неактивен' },
  { value: 'under_renovation', label: 'На реконструкции' },
];

export const UNIT_STATUSES = [
  { value: 'available', label: 'Доступен' },
  { value: 'not_available', label: 'Недоступен' },
  { value: 'under_maintenance', label: 'На обслуживании' },
];

export const BED_TYPES = [
  { value: 'single', label: 'Односпальная' },
  { value: 'double', label: 'Двуспальная' },
  { value: 'queen', label: 'Queen' },
  { value: 'king', label: 'King' },
  { value: 'california_king', label: 'California King' },
  { value: 'bunk_bed', label: 'Двухъярусная' },
  { value: 'sofa', label: 'Диван' },
  { value: 'pull_out_sofa', label: 'Раскладной диван' },
  { value: 'futon', label: 'Футон' },
  { value: 'adjustable_bed', label: 'Регулируемая кровать' },
];

export const BOOKING_STATUS_LABELS = {
  pending: 'Ожидает подтверждения',
  confirmed: 'Подтверждено',
  cancelled: 'Отменено',
  completed: 'Завершено',
  rejected: 'Отклонено',
};

export const ROLE_LABELS = {
  user: 'Гость',
  owner: 'Владелец',
  admin: 'Администратор',
};

export function labelFor(list, value) {
  return list.find((i) => i.value === value)?.label || value;
}
