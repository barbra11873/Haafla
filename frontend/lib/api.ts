import axios from 'axios'

export const api = axios.create({
  baseURL: 'http://localhost:8000/api',
})

api.interceptors.request.use((config) => {
  if (typeof window === 'undefined') return config
  const token = localStorage.getItem('access')
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const getMe = async () => {
  const res = await api.get('/accounts/me/')
  return res.data
}

export default api
