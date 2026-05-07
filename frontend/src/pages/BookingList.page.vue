<template>
  <div>
    <h1>Kölcsönzéseim</h1>

    <div class="search-container">
      Kereses: <input type="text" v-model="search" @input="fetchLoans()" />
    </div>

    <div v-if="loading">Betöltés...</div>

    <ul v-else-if="loans.length">
      <li v-for="loan in loans" :key="loan.loan_id" @click="() => router.push(`/bookings/${loan.loan_id}`)"
        style="border-bottom: 1px solid #ddd; padding: 10px 0;">
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
  margin: 12px 0;
}
</style>