import { defineStore } from 'pinia';
import { apiClient } from '../api-client/api.client';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    userId: localStorage.getItem('user_id') || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(email, password) {
      const response = await apiClient.post('/api/auth/login', { email, password });
      this.token = response.data.token;
      this.userId = response.data.user_id;
      this.user = { 
        email: response.data.email, 
        name: response.data.name, 
        role: response.data.role 
      };
      
      localStorage.setItem('token', this.token);
      localStorage.setItem('user_id', this.userId);
    },
    async register(userData) {
      await apiClient.post('/api/auth/register', userData);
    },
    async logout() {
      try {
        if (this.token) {
          await apiClient.post('/api/auth/logout');
        }
      } catch (e) {
        console.error('Kijelentkezési hiba:', e);
      } finally {
        this.token = null;
        this.user = null;
        this.userId = null;
        localStorage.removeItem('token');
        localStorage.removeItem('user_id');
      }
    }
  }
});