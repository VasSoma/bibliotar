import { defineStore } from 'pinia';
import { apiClient } from '../api-client/api.client';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    userId: localStorage.getItem('user_id') ? Number(localStorage.getItem('user_id')) : null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(email, password) {
      try {
        const response = await apiClient.post('/auth/login', { email, password });
        const token = response.data.token;
        
        let rawId = response.data.user_id || response.data.userId;
        if (!rawId && token) {
          try {
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const payload = JSON.parse(window.atob(base64));
            rawId = payload.user_id || payload.sub;
            console.log('ID kinyerve a tokenből:', rawId);
          } catch (e) {
            console.error('Nem sikerült dekódolni a tokent:', e);
          }
        }

        this.token = token;
        this.userId = rawId ? Number(rawId) : null;
        
        this.user = { 
          email: response.data.email, 
          name: response.data.name, 
          role: response.data.role 
        };
        
        localStorage.setItem('token', this.token);
        if (this.userId) {
          localStorage.setItem('user_id', String(this.userId));
        }

        return response.data;
      } catch (error) {
        console.error('Bejelentkezési hiba:', error);
        throw error;
      }
    },
    async logout() {
      try {
        if (this.token) await apiClient.post('/auth/logout');
      } finally {
        this.token = null;
        this.userId = null;
        this.user = null;
        localStorage.removeItem('token');
        localStorage.removeItem('user_id');
        window.location.href = '/login';
      }
    }
  }
});