<template>
  <div>
    <h1>Saját Profil</h1>
    <section v-if="profile">
      <h2>Személyes adatok módosítása</h2>
      <form @submit.prevent="updateProfile">
        <label>Név: <input v-model="profile.name" type="text" /></label>
        <label>Email: <input v-model="profile.email" type="email" /></label>
        <label>Telefon: <input v-model="profile.phone_number" type="text" /></label>
        
        <fieldset>
          <legend>Cím</legend>
          <label>Irányítószám: <input v-model="profile.address.postal_code" type="text" /></label>
          <label>Város: <input v-model="profile.address.city" type="text" /></label>
          <label>Utca: <input v-model="profile.address.street" type="text" /></label>
          <label>Házszám: <input v-model="profile.address.house_number" type="text" /></label>
          <label>Megye: <input v-model="profile.address.county" type="text" /></label>
        </fieldset>
        
        <button type="submit">Adatok frissítése</button>
      </form>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { apiClient } from '../api-client/api.client';

const profile = ref(null);

const fetchProfile = async () => {
  try {
    const res = await apiClient.get('/api/user/profile');
    profile.value = res.data;
  } catch (error) {
    console.error('Profil lekérdezési hiba', error);
  }
};

const updateProfile = async () => {
  try {
    await apiClient.patch('/api/user/profile', {
      name: profile.value.name,
      email: profile.value.email,
      phone_number: profile.value.phone_number,
      address: profile.value.address
    });
    alert('Profil sikeresen frissítve!');
  } catch (error) {
    alert('Hiba a frissítés során.');
  }
};

onMounted(() => {
  fetchProfile();
});
</script>