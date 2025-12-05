import axios from 'axios'

// Use environment variable for API URL, fallback to relative path
// When served from same domain (production), use relative path
// When in development, vite proxy handles it
const API_BASE_URL = import.meta.env.VITE_API_URL || ''

const api = axios.create({
  baseURL: API_BASE_URL ? `${API_BASE_URL}/api` : '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API methods
export const workflowAPI = {
  run: (spec: Record<string, unknown>) => api.post('/run', spec),
  plan: (spec: Record<string, unknown>) => api.post('/plan', spec),
  list: () => api.get('/workflows'),
  get: (id: string) => api.get(`/workflows/${id}`),
}

export const llmAPI = {
  plan: (spec: Record<string, unknown>) => api.post('/llm/plan', spec),
  recovery: (error: string, context: Record<string, unknown>) =>
    api.post('/llm/recovery', { error, context }),
  validate: (spec: Record<string, unknown>) => api.post('/llm/validate', spec),
}

export const pluginAPI = {
  list: () => api.get('/plugins'),
  get: (name: string) => api.get(`/plugins/${name}`),
}

export const auditAPI = {
  list: (params?: Record<string, unknown>) => api.get('/audit', { params }),
  export: () => api.get('/audit/export'),
}

export const healthAPI = {
  check: () => api.get('/health'),
  metrics: () => api.get('/metrics'),
}

export default api
