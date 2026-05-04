<template>
  <header>
    <nav>
      <router-link to="/">Főoldal</router-link>
      <router-link to="/books">Könyvek</router-link>
      
      <template v-if="authStore.isAuthenticated">
        <router-link to="/profile">Saját profil</router-link>
        <button @click="handleLogout">Kijelentkezés</button>
      </template>
      
      <template v-else>
        <router-link to="/login">Bejelentkezés / Regisztráció</router-link>
      </template>
    </nav>
  </header>
</template>

<script setup>
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};
</script>