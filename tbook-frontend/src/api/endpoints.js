import client from './client';

/* ---------------- Auth / users ---------------- */
export const authApi = {
  register: (payload) => client.post('/users/register/', payload),
  login: (payload) => client.post('/users/login/', payload),
  profile: () => client.get('/users/profile/'),
  updateProfile: (payload) => client.patch('/users/profile/', payload),
  changePassword: (payload) => client.post('/users/change-password/', payload),
};

/* ---------------- Public listings (guest browsing) ---------------- */
export const listingsApi = {
  list: (params) => client.get('/listings/', { params }),
  detail: (propertyUuid, params) => client.get(`/listings/${propertyUuid}/`, { params }),
};

/* ---------------- Property catalogs ---------------- */
export const catalogApi = {
  amenities: () => client.get('/property/amenities/'),
  bedTypes: () => client.get('/property/beds/types/'),
};

/* ---------------- Owner: properties ---------------- */
export const propertyApi = {
  list: () => client.get('/property/'),
  create: (payload) => client.post('/property/', payload),
  detail: (propertyUuid) => client.get(`/property/${propertyUuid}/`),
  update: (propertyUuid, payload) => client.patch(`/property/${propertyUuid}/`, payload),
  remove: (propertyUuid) => client.delete(`/property/${propertyUuid}/`),
};

/* ---------------- Owner: units ---------------- */
export const unitApi = {
  list: (propertyUuid) => client.get(`/property/${propertyUuid}/units/`),
  create: (propertyUuid, payload) => client.post(`/property/${propertyUuid}/units/`, payload),
  detail: (propertyUuid, unitUuid) => client.get(`/property/${propertyUuid}/units/${unitUuid}/`),
  update: (propertyUuid, unitUuid, payload) =>
    client.patch(`/property/${propertyUuid}/units/${unitUuid}/`, payload),
  remove: (propertyUuid, unitUuid) => client.delete(`/property/${propertyUuid}/units/${unitUuid}/`),
};

/* ---------------- Bookings: guest side ---------------- */
export const bookingApi = {
  create: (payload) => client.post('/bookings/', payload),
  active: () => client.get('/bookings/'),
  all: () => client.get('/bookings/all/'),
  completed: () => client.get('/bookings/completed/'),
  cancelledRejected: () => client.get('/bookings/cancelled-rejected/'),
  detail: (bookingUuid) => client.get(`/bookings/${bookingUuid}/`),
  cancel: (bookingUuid) => client.post(`/bookings/${bookingUuid}/cancel/`),
};

/* ---------------- Bookings: owner side ---------------- */
export const ownerBookingApi = {
  active: () => client.get('/owner/bookings/'),
  pending: () => client.get('/owner/bookings/pending/'),
  confirmed: () => client.get('/owner/bookings/confirmed/'),
  completed: () => client.get('/owner/bookings/completed/'),
  cancelledRejected: () => client.get('/owner/bookings/cancelled-rejected/'),
  all: () => client.get('/owner/bookings/all/'),
  detail: (bookingUuid) => client.get(`/owner/bookings/${bookingUuid}/`),
  confirm: (bookingUuid) => client.post(`/owner/bookings/${bookingUuid}/confirm/`),
  reject: (bookingUuid) => client.post(`/owner/bookings/${bookingUuid}/reject/`),
  complete: (bookingUuid) => client.post(`/owner/bookings/${bookingUuid}/complete/`),
};

/* ---------------- Reviews ---------------- */
export const reviewApi = {
  list: () => client.get('/reviews/'),
  create: (payload) => client.post('/reviews/', payload),
  detail: (reviewUuid) => client.get(`/reviews/${reviewUuid}/`),
  update: (reviewUuid, payload) => client.patch(`/reviews/${reviewUuid}/`, payload),
  remove: (reviewUuid) => client.delete(`/reviews/${reviewUuid}/`),
};

/* ---------------- Media: property images ---------------- */
export const propertyImageApi = {
  upload: (propertyUuid, files) => {
    const form = new FormData();
    files.forEach((f) => form.append('images', f));
    return client.post(`/media/${propertyUuid}/images/`, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  remove: (propertyUuid, imageUuid) => client.delete(`/media/${propertyUuid}/images/${imageUuid}/`),
  setCover: (propertyUuid, imageUuid) => client.post(`/media/${propertyUuid}/images/${imageUuid}/cover/`),
  setOrder: (propertyUuid, imageUuid, ordering) =>
    client.post(`/media/${propertyUuid}/images/ordering/`, { uuid: imageUuid, ordering }),
};

/* ---------------- Media: unit images ---------------- */
export const unitImageApi = {
  upload: (propertyUuid, unitUuid, files) => {
    const form = new FormData();
    files.forEach((f) => form.append('images', f));
    return client.post(`/media/${propertyUuid}/units/${unitUuid}/images/`, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  remove: (propertyUuid, unitUuid, imageUuid) =>
    client.delete(`/media/${propertyUuid}/units/${unitUuid}/images/${imageUuid}/`),
  setCover: (propertyUuid, unitUuid, imageUuid) =>
    client.post(`/media/${propertyUuid}/units/${unitUuid}/images/${imageUuid}/cover/`),
  setOrder: (propertyUuid, unitUuid, imageUuid, ordering) =>
    client.post(`/media/${propertyUuid}/units/${unitUuid}/images/ordering/`, { uuid: imageUuid, ordering }),
};
