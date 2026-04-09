import axios from 'axios';

// Instancia global del API
// En producción apuntará al dominio público, en dev al localhost dictado por Vite
export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Interceptor para embeber en un futuro el JWT del cliente sin repetir código
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('user_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);
