<template>
  <div>
    <h1>Kölcsönzéseim</h1>

    <div v-if="loading">Betöltés...</div>
    
    <ul v-else-if="loans.length">
      <li v-for="loan in loans" :key="loan.loan_id" style="border-bottom: 1px solid #ddd; padding: 10px 0;">
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
        
        <div v-if="!loan.return_date">
          <button 
            @click="extendLoan(loan.loan_id)" 
            :disabled="loan.extension_count >= 2">
            Hosszabbítás
          </button>
          
          <button @click="returnBook(loan.loan_id)" style="margin-left: 10px;">
            Visszahozatal
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
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const loans = ref([]);
const loading = ref(false);

const fetchLoans = async () => {
  if (!authStore.userId) return;
  loading.value = true;
  try {
    const res = await apiClient.get(`/loans/history/${authStore.userId}`);
    loans.value = res.data;
  } catch (error) {
    console.error('Kölcsönzések betöltési hiba:', error);
  } finally {
    loading.value = false;
  }
};

const extendLoan = async (loanId) => {
  try {
    await apiClient.post(`/loans/history/${loanId}/extend`);
    alert('Sikeres hosszabbítás!');
    fetchLoans();
  } catch (error) {
    alert(error.response?.data?.message || 'Nem sikerült a hosszabbítás.');
  }
};

const rentBook = async (bookId) => {
  console.log('UserID a store-ban:', authStore.userId);

  if (!authStore.userId || isNaN(authStore.userId)) {
    alert("Hiba: Érvénytelen felhasználói azonosító! Kérlek jelentkezz be újra.");
    return;
  }

  try {
    await apiClient.post('/loans/history/create', {
      book_id: Number(bookId),
      user_id: Number(authStore.userId)
    });
    alert('Sikeres kölcsönzés!');
    fetchBooks();
  } catch (error) {
    alert('Hiba: ' + (error.response?.data?.message || 'Sikertelen tranzakció'));
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