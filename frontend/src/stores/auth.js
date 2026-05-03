import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { api } from '@/api-client/api.client'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthenticated = computed(() => !!user.value)
  const role = ref(null)
  const error = ref(null)

  const login = async (credentials) => {
    try {
      const res = await api.post('/auth/login', credentials)
      localStorage.setItem('token', res.data.token)
      await fetchUser()
      router.push('/books')
    } catch (err) {
      error.value = 'Invalid email or password.'
    }
  }

  const logout = async () => {
    await api.post('/auth/logout')

    localStorage.removeItem('token')
    user.value = null
    router.push('/login')
  }

  const fetchUser = async () => {
    try {
      const res = await api.get('/user/profile')
      user.value = res.data
      role.value = res.data.role
    } catch {
      user.value = null
      router.push('/login')
    }
  }

  const hasRole = (requiredRoles) => {
    if (!requiredRoles?.length) {
      return true
    }

    return requiredRoles.includes(role.value)
  }

  return { isAuthenticated, error, login, logout, fetchUser, hasRole }
})