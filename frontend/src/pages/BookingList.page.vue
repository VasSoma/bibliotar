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

        <span v-if="authStore.user?.role === 'librarian' || authStore.user?.role === 'admin'" style="color: blue;">
          (Kölcsönző: {{ loan.user?.name }} – {{ loan.user?.email }})
        </span>

        <ul>
          <li>Kezdet: {{ formatDate(loan.start_date) }}</li>
          <li>Határidő: {{ formatDate(loan.due_date) }}</li>
          <li v-if="loan.return_date">
            <span v-if="loan.return_date" :style="{ color: isReturnedLate(loan) ? 'red' : 'green', fontWeight: 'bold' }">Visszahozva: {{ formatDate(loan.return_date) }}</span>
          </li>
          <li>
            Hosszabbítások: {{ loan.extension_count }}
            <span v-if="authStore.user?.role !== 'librarian'"> / 2</span>
          </li>
          <li v-if="loan.overdue_fine > 0" style="font-weight: bold;">
            <span v-if="loan.fine_is_paid" style="color: green;">
              Bírság rendezve: <span style="color: red;"> {{ loan.overdue_fine }}</span> <span> Ft</span>
            </span>
            <span v-else style="color: red;">
              Büntetés: {{ loan.overdue_fine }} Ft
            </span>
          </li>
        </ul>

        <div style="margin-top: 10px; display: flex; gap: 8px; flex-wrap: wrap;" @click.stop>
          <button
            v-if="!loan.return_date && (loan.extension_count < 2 || authStore.user?.role === 'librarian')"
            @click="extendLoan(loan.loan_id)"
            class="extend-btn"
          >
            Hosszabbítás
            <span v-if="authStore.user?.role === 'librarian'">(+7 nap)</span>
            <span v-else>(+1 nap)</span>
          </button>

          <span v-else-if="!loan.return_date && loan.extension_count >= 2 && authStore.user?.role !== 'librarian'" style="color: gray; font-size: 0.9em;">
            Maximális hosszabbítás elérve.
          </span>

          <button
            v-if="authStore.user?.role === 'librarian' && !loan.return_date"
            @click="returnLoan(loan.loan_id)"
            style="background-color: #4caf50; color: white;"
          >
            Könyv visszavétele
          </button>

          <button
            v-if="authStore.user?.role === 'librarian' && loan.overdue_fine > 0 && loan.return_date && !loan.fine_is_paid"
            @click="markFinePaid(loan.loan_id)"
            style="background-color: #ff9800; color: white;"
          >
            Bírság rendezése
          </button>
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

const router = useRouter();
const authStore = useAuthStore();
const loans = ref([]);
const loading = ref(false);
const search = ref('');

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

const extendLoan = async (loanId) => {
  try {
    await apiClient.post(`/loans/${loanId}/extend`);
    alert('A kölcsönzési időt sikeresen meghosszabbítottuk!');
    fetchLoans();
  } catch (error) {
    alert('Hiba: ' + (error.response?.data?.message || 'Hosszabbítás sikertelen.'));
  }
};

const returnLoan = async (loanId) => {
  if (!confirm('Biztosan visszaveszed ezt a könyvet?')) return;
  try {
    await apiClient.post(`/loans/${loanId}/returned`);
    alert('Könyv sikeresen visszavéve.');
    fetchLoans();
  } catch (error) {
    alert('Hiba: ' + (error.response?.data?.message || 'Visszavétel sikertelen.'));
  }
};

const markFinePaid = async (loanId) => {
  if (!confirm('Biztosan rendezettnek jelölöd a bírságot?')) return;
  try {
    await apiClient.post(`/loans/${loanId}/fine_paid`);
    alert('Bírság rendezése.');
    fetchLoans();
  } catch (error) {
    alert('Hiba: ' + (error.response?.data?.message || 'Bírság jelölés sikertelen.'));
  }
};

const formatDate = (dateStr) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleDateString('hu-HU');
};

const isReturnedLate = (loan) => {
    return new Date(loan.return_date) > new Date(loan.due_date);
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
