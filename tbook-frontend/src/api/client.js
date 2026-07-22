import axios from 'axios';

// Same-origin by default: in prod Nginx serves this app AND proxies /api,
// so a relative base URL avoids CORS entirely. Overridable at build time.
export const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const ACCESS_KEY = 'tbook_access';
const REFRESH_KEY = 'tbook_refresh';

export const tokenStore = {
  get access() {
    return localStorage.getItem(ACCESS_KEY);
  },
  get refresh() {
    return localStorage.getItem(REFRESH_KEY);
  },
  set({ access, refresh }) {
    if (access) localStorage.setItem(ACCESS_KEY, access);
    if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
  },
  clear() {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
  },
};

const client = axios.create({ baseURL: API_BASE });

client.interceptors.request.use((config) => {
  const access = tokenStore.access;
  if (access) config.headers.Authorization = `Bearer ${access}`;
  return config;
});

let refreshPromise = null;

client.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;
    const status = error.response?.status;
    const isAuthEndpoint = original?.url?.includes('/users/login') || original?.url?.includes('/users/token/refresh');

    if (status === 401 && !original._retry && !isAuthEndpoint) {
      original._retry = true;
      const refresh = tokenStore.refresh;
      if (!refresh) {
        tokenStore.clear();
        window.dispatchEvent(new Event('tbook:unauthorized'));
        return Promise.reject(error);
      }
      try {
        if (!refreshPromise) {
          refreshPromise = axios
            .post(`${API_BASE}/users/token/refresh/`, { refresh })
            .finally(() => {
              refreshPromise = null;
            });
        }
        const { data } = await refreshPromise;
        tokenStore.set({ access: data.access });
        original.headers.Authorization = `Bearer ${data.access}`;
        return client(original);
      } catch (e) {
        tokenStore.clear();
        window.dispatchEvent(new Event('tbook:unauthorized'));
        return Promise.reject(e);
      }
    }
    return Promise.reject(error);
  }
);

export function apiErrorMessage(err, fallback = 'Что-то пошло не так. Попробуйте ещё раз.') {
  const data = err?.response?.data;
  if (!data) return err?.message || fallback;
  if (typeof data === 'string') return data;
  if (data.error) return data.error;
  if (data.detail) return data.detail;
  // DRF validation errors: { field: [msg, ...] } or { field: "msg" }
  const parts = [];
  for (const [key, val] of Object.entries(data)) {
    const msg = Array.isArray(val) ? val.join(' ') : val;
    parts.push(key === 'non_field_errors' ? msg : `${key}: ${msg}`);
  }
  return parts.length ? parts.join(' | ') : fallback;
}

export default client;
