<template>
  <div class="login-container">
    <h2>Bejelentkezés</h2>
    <form @submit.prevent="handleSubmit">
      <div>
        <label for="login-email">Email cím:</label>
        <input 
          id="login-email" 
          name="email" 
          type="email" 
          v-model="email" 
          autocomplete="email" 
          required 
        />
      </div>
      <div>
        <label for="login-password">Jelszó:</label>
        <input 
          id="login-password" 
          name="password" 
          type="password" 
          v-model="password" 
          autocomplete="current-password" 
          required 
        />
      </div>
      <button type="submit">Belépés</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const email = ref('');
const password = ref('');

const handleSubmit = async () => {
  try {
    await authStore.login(email.value, password.value);
    router.push('/');
  } catch (error) {
    alert('Hiba a bejelentkezés során: ' + (error.response?.data?.message || 'Hibás adatok'));
  }
};
</script>

