<template>
  <div>
    <h1>Saját Profil</h1>
    <section v-if="profile">
      <h2>Személyes adatok</h2>

      <div v-if="!isBeingEdited">
        <p><strong>Név:</strong> {{ profile.name }}</p>
        <p><strong>Email:</strong> {{ profile.email }}</p>
        <p><strong>Telefon:</strong> {{ profile.phone_number }}</p>
        <fieldset>
          <legend>Cím</legend>
          <p><strong>Irányítószám:</strong> {{ profile.address?.postal_code }}</p>
          <p><strong>Város:</strong> {{ profile.address?.city }}</p>
          <p><strong>Utca:</strong> {{ profile.address?.street }}</p>
          <p><strong>Házszám:</strong> {{ profile.address?.house_number }}</p>
          <p><strong>Megye:</strong> {{ profile.address?.county }}</p>
        </fieldset>
        <button @click="() => isBeingEdited = true">Szerkesztés</button>
      </div>

      <form v-if="isBeingEdited" @submit.prevent="updateProfile">
        <p><strong>Név:</strong> <input v-model="profile.name" type="text" /></p>
        <p><strong>Email:</strong> <input v-model="profile.email" type="email" /></p>
        <p><strong>Telefon:</strong> <input v-model="profile.phone_number" type="text" /></p>
        <fieldset>
          <legend>Cím</legend>
          <p><strong>Irányítószám:</strong> <input v-model="profile.address.postal_code" type="text" /></p>
          <p><strong>Város:</strong> <input v-model="profile.address.city" type="text" /></p>
          <p><strong>Utca:</strong> <input v-model="profile.address.street" type="text" /></p>
          <p><strong>Házszám:</strong> <input v-model="profile.address.house_number" type="text" /></p>
          <p><strong>Megye:</strong> <input v-model="profile.address.county" type="text" /></p>
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
const isBeingEdited = ref(false)

const fetchProfile = async () => {
  try {
    const res = await apiClient.get('/user/profile');
    profile.value = res.data;
  } catch (error) {
    console.error('Profil lekérdezési hiba', error);
  }
};

const updateProfile = async () => {
  try {
    await apiClient.patch('/user/profile', {
      name: profile.value.name,
      email: profile.value.email,
      phone_number: profile.value.phone_number,
      address: profile.value.address
    });
    alert('Profil sikeresen frissítve!');
    isBeingEdited.value = false
  } catch (error) {
    alert('Hiba a frissítés során.');
  }
};

onMounted(() => {
  fetchProfile();
});
</script>