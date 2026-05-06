import { defineStore } from 'pinia'
import { apiClient } from '../api-client/api.client'
import { ref, computed } from 'vue'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthenticated = computed(() => !!user.value)
  const error = ref(null)

  const login = async (credentials) => {
    try {
      const res = await apiClient.post('/auth/login', credentials)
      localStorage.setItem('token', res.data.token)
      await fetchUser()
      router.push('/books')
    } catch (err) {
      error.value = 'Invalid email or password.'
    }
  }

  const register = async (payload) => {
    try {
      await apiClient.post('/auth/register', payload)
    } catch (error) {
      error.value = 'Cannot register user right now.'
    }
  }

  const logout = async () => {
    await apiClient.post('/auth/logout')

    localStorage.removeItem('token')
    user.value = null
    router.push('/login')
  }

  const fetchUser = async () => {
    try {
      const res = await apiClient.get('/user/profile')
      user.value = res.data
    } catch {
      user.value = null
      router.push('/login')
    }
  }

  const hasRole = (requiredRoles) => {
    if (!requiredRoles?.length) {
      return true
    }

    return requiredRoles.includes(user.value.role)
  }

  return { user, isAuthenticated, error, login, register, logout, fetchUser, hasRole }
})