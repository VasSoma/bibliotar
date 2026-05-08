<template>
  <div>
    <h1>Kölcsönzéseim / Rendszer kölcsönzései</h1>

    <div class="search-container">
      Keresés: <input type="text" v-model="search" @input="fetchLoans()" placeholder="Keresés..." />
    </div>

    <div v-if="loading">Betöltés...</div>

    <ul v-else-if="loans.length">
      <li v-for="loan in loans" :key="loan.loan_id" @click="() => router.push(`/bookings/${loan.loan_id}`)"
        style="border-bottom: 1px solid #ddd; padding: 10px 0; cursor: pointer;">
        
        <strong>{{ loan.book?.title }}</strong> - {{ loan.book?.author }}
        
        <span v-if="authStore.user?.role === 'librarian'" style="color: blue;"> 
          (Kölcsönző: {{ loan.user?.email || loan.user_email || 'A backend nem küldi az emailt' }})
        </span>
        
        <ul>
          <li>Kezdet: {{ formatDate(loan.start_date) }}</li>
          <li>Határidő: {{ formatDate(loan.due_date) }}</li>
          <li v-if="loan.return_date">Visszahozva: {{ formatDate(loan.return_date) }}</li>
          <li>Hosszabbítások: {{ loan.extension_count }} <span v-if="authStore.user?.role !== 'librarian'">/ 2</span></li>
          <li v-if="loan.overdue_fine > 0" style="color: red; font-weight: bold;">
            Büntetés: {{ loan.overdue_fine }} Ft
          </li>
        </ul>

        <div style="margin-top: 10px;">
          <button 
            v-if="!loan.return_date && (loan.extension_count < 2 || authStore.user?.role === 'librarian')" 
            @click.stop="extendLoan(loan.loan_id)"
            class="extend-btn"
          >
            Hosszabbítás (+14 nap)
          </button>
          
          <span v-else-if="!loan.return_date && loan.extension_count >= 2 && authStore.user?.role !== 'librarian'" style="color: gray; font-size: 0.9em;">
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
import { useAuthStore } from '../stores/auth';

const router = useRouter()
const authStore = useAuthStore()
const loans = ref([]);
const loading = ref(false);
const search = ref("");

const fetchLoans = async () => {
  loading.value = true;
  try {
    const res = await apiClient.get(search.value ? `/loans?search=${search.value}` : '/loans');
    loans.value = res.data;
  } catch (error) {
    console.error('Kölcsönzések betöltési hiba. A backend a hibás!', error);
  } finally {
    loading.value = false;
  }
};

const extendLoan = async (loanId) => {
  try {
    await apiClient.post(`/loans/history/${loanId}/extend`);
    alert('A kölcsönzési időt sikeresen meghosszabbítottuk!');
    fetchLoans();
  } catch (error) {
    alert('Sikertelen hosszabbítás! A backend a hibás!');
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

<style>
.search-container {
  margin-bottom: 20px;
}
</style>