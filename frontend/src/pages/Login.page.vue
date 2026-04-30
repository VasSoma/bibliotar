<template>
  <div>
    <h2>{{ isLogin ? 'Bejelentkezés' : 'Regisztráció' }}</h2>
    
    <form @submit.prevent="handleSubmit">
      <div v-if="!isLogin">
        <label>Név:</label>
        <input v-model="formData.name" type="text" required />
      </div>
      
      <div>
        <label>Email:</label>
        <input v-model="formData.email" type="email" required />
      </div>
      
      <div>
        <label>Jelszó:</label>
        <input v-model="formData.password" type="password" required />
      </div>

      <div v-if="!isLogin">
        <label>Telefonszám:</label>
        <input v-model="formData.phone_number" type="text" />
        
        <fieldset>
          <legend>Lakcím</legend>
          <label>Irányítószám: <input v-model="formData.address.postal_code" type="text" /></label>
          <label>Város: <input v-model="formData.address.city" type="text" /></label>
          <label>Utca: <input v-model="formData.address.street" type="text" /></label>
          <label>Házszám: <input v-model="formData.address.house_number" type="text" /></label>
          <label>Megye: <input v-model="formData.address.county" type="text" /></label>
        </fieldset>
      </div>

      <button type="submit">{{ isLogin ? 'Belépés' : 'Regisztrálok' }}</button>
    </form>
    
    <button @click="isLogin = !isLogin">
      {{ isLogin ? 'Nincs még fiókod? Regisztrálj!' : 'Már van fiókod? Lépj be!' }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const isLogin = ref(true);
const formData = ref({
  email: '',
  password: '',
  name: '',
  phone_number: '',
  address: { city: '', county: '', house_number: '', postal_code: '', street: '' }
});

const handleSubmit = async () => {
  try {
    if (isLogin.value) {
      await authStore.login(formData.value.email, formData.value.password);
    } else {
      await authStore.register(formData.value);
      await authStore.login(formData.value.email, formData.value.password);
    }
    router.push('/profile');
  } catch (error) {
    alert('Hiba történt a művelet során: ' + (error.response?.data?.message || error.message));
  }
};
</script>