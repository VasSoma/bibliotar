<template>
  <header>
    <nav class="nav">
      <template v-if="authStore.isAuthenticated">
      <router-link to="/">Főoldal</router-link>
      <router-link to="/books">Könyvek</router-link>
      <router-link to="/bookings">Kölcsönzések</router-link>
        <router-link to="/profile">Saját profil</router-link>
        <button @click="handleLogout">Kijelentkezés</button>
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

<style>
.nav {display: flex; gap: 8px;}
</style>