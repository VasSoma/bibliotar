<template>
  <div class="register-container">
    <h2>Regisztráció</h2>
    <form @submit.prevent="handleSubmit">
      <div>
        <label for="reg-name">Teljes név:</label>
        <input id="reg-name" name="name" type="text" v-model="formData.name" autocomplete="name" required />
      </div>
      <div>
        <label for="reg-email">Email:</label>
        <input id="reg-email" name="email" type="email" v-model="formData.email" autocomplete="email" required />
      </div>
      <div>
        <label for="reg-password">Jelszó:</label>
        <input id="reg-password" name="password" type="password" v-model="formData.password" autocomplete="new-password" required />
      </div>
      <div>
        <label for="reg-phone">Telefonszám:</label>
        <input id="reg-phone" name="phone_number" type="tel" v-model="formData.phone_number" autocomplete="tel" />
      </div>

      <fieldset>
        <legend>Lakcím adatai</legend>
        <div>
          <label for="reg-pc">Irányítószám:</label>
          <input id="reg-pc" name="postal-code" type="text" v-model="formData.address.postal_code" autocomplete="postal-code" required />
        </div>
        <div>
          <label for="reg-city">Város:</label>
          <input id="reg-city" name="city" type="text" v-model="formData.address.city" autocomplete="address-level2" required />
        </div>
        <div>
          <label for="reg-street">Utca:</label>
          <input id="reg-street" name="street" type="text" v-model="formData.address.street" autocomplete="address-line1" required />
        </div>
        <div>
          <label for="reg-hn">Házszám:</label>
          <input id="reg-hn" name="house-number" type="text" v-model="formData.address.house_number" required />
        </div>
        <div>
          <label for="reg-county">Megye:</label>
          <input id="reg-county" name="county" type="text" v-model="formData.address.county" autocomplete="address-level1" required />
        </div>
      </fieldset>

      <button type="submit">Regisztrálok</button>
    </form>
    <button @click="$router.push('/login')">Már van fiókom, belépek</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const formData = ref({
  email: '',
  password: '',
  name: '',
  phone_number: '',
  address: { 
    city: '', 
    county: '', 
    house_number: '', 
    postal_code: '', 
    street: '' 
  }
});

const handleSubmit = async () => {
  try {
    console.log('Regisztrációs adatok küldése:', JSON.parse(JSON.stringify(formData.value)));
    await authStore.register(formData.value);
    alert('Sikeres regisztráció!');
    router.push('/login');
  } catch (error) {
    if (error.response) {
      // A szerver válaszolt valamit (pl. 422, 400, 500)
      console.error('Backend hibaadatok:', error.response.data);
      console.error('Status kód:', error.response.status);
      alert('Szerver hiba: ' + JSON.stringify(error.response.data.detail || error.response.data.message));
    } else if (error.request) {
      // A kérés kiment, de nem jött válasz (pl. hálózati hiba vagy CORS)
      console.error('Nem érkezett válasz a szervertől. Ellenőrizd a CORS beállításokat vagy fut-e a backend!');
      alert('A szerver nem elérhető.');
    } else {
      // Valami elszállt a kérés összeállításakor
      console.error('Kód hiba:', error.message);
    }
  }
};
</script>