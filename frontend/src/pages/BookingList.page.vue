<template>
  <div>
    <h1>Kölcsönzéseim</h1>

    <div class="search-container">
      Kereses: <input type="text" v-model="search" @input="fetchLoans()" />
    </div>

    <div v-if="loading">Betöltés...</div>

    <ul v-else-if="loans.length">
      <li v-for="loan in loans" :key="loan.loan_id" @click="() => router.push(`/bookings/${loan.loan_id}`)"
        style="border-bottom: 1px solid #ddd; padding: 10px 0; cursor: pointer;">
        <strong>{{ loan.book.title }}</strong> - {{ loan.book.author }}
        <ul>
          <li>Kezdet: {{ formatDate(loan.start_date) }}</li>
          <li>Határidő: {{ formatDate(loan.due_date) }}</li>
          <li v-if="loan.return_date">Visszahozva: {{ formatDate(loan.return_date) }}</li>
          <li>Hosszabbítások: {{ loan.extension_count }} / 2</li>
          <li v-if="loan.overdue_fine > 0" style="color: red; font-weight: bold;">
            Büntetés: {{ loan.overdue_fine }} Ft
          </li>
        </ul>

        <div style="margin-top: 10px;">
          <button 
            v-if="!loan.return_date && loan.extension_count < 2" 
            @click.stop="extendLoan(loan.loan_id)"
            class="extend-btn"
          >
            Hosszabbítás (+14 nap)
          </button>
          <span v-else-if="!loan.return_date && loan.extension_count >= 2" style="color: gray; font-size: 0.9em;">
            Maximális hosszabbítás elérve.
          </span>
        </div>

      </li>
    </ul>

    <p v-else>Nincsenek aktív vagy korábbi kölcsönzések.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { apiClient } from '../api-client/api.client';
import { useRouter } from 'vue-router';

const router = useRouter()
const loans = ref([]);
const loading = ref(false);
const search = ref("");

const fetchLoans = async () => {
  loading.value = true;
  try {
    const res = await apiClient.get(search.value ? `/loans?search=${search.value}` : '/loans');
    loans.value = res.data;
  } catch (error) {
    console.error('Kölcsönzések betöltési hiba:', error);
  } finally {
    loading.value = false;
  }
};

// ÚJ RÉSZ: Hosszabbítás API hívás
const extendLoan = async (loanId) => {
  try {
    // Feltételezem, hogy a backend végpontod valami ilyesmi lett: /loans/<id>/extend
    await apiClient.post(`/loans/${loanId}/extend`);
    alert('A kölcsönzési időt sikeresen meghosszabbítottuk!');
    
    // Lista újratöltése, hogy frissüljön a határidő és a számláló
    fetchLoans();
  } catch (error) {
    console.error('Hiba a hosszabbítás során:', error);
    
    // Ha a backend valamilyen hibaüzenetet küld (pl. 400 Bad Request), azt itt kiírhatod
    if (error.response && error.response.data && error.response.data.message) {
      alert(`Hiba: ${error.response.data.message}`);
    } else {
      alert('Váratlan hiba történt a hosszabbítás során.');
    }
  }
};

const formatDate = (dateStr) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleDateString('hu-HU');
};

onMounted(() => {
  fetchLoans();
});
</script>