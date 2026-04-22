<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const email = ref('')
const password = ref('')

const handleLogin = async () => {
  await auth.login({ email: email.value, password: password.value })
}
</script>

<template>
  <form @submit.prevent="handleLogin" class="form">
    <h2>Login</h2>

    <input v-model="email" type="email" placeholder="Email" required />

    <input v-model="password" type="password" placeholder="Password" required />

    <button type="submit">Login</button>

    <p v-if="auth.error" class="error">{{ auth.error }}</p>
  </form>
</template>

<style>
.form {
  width: 400px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.error {
  color: red;
}
</style>