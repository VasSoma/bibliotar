import { api } from '@/api-client/api.client'
import router from '@/router'

export const setupApiClient = () => {
  api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  })

  api.interceptors.response.use(
    (res) => res,
    (error) => {
      if (error.response?.status === 401) {
        localStorage.removeItem('token')
        router.push('/login')
      }

      return Promise.reject(error)
    },
  )
}