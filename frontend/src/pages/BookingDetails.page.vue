<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { apiClient } from '@/api-client/api.client'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const loanId = route.params.id
const loan = ref(null)
const authStore = useAuthStore()

onMounted(async () => {
  fetchLoan()
})

async function fetchLoan() {
  const { data } = await apiClient.get(`/loans/${loanId}`)
  loan.value = data
}

async function returnBook() {
  try {
    await apiClient.post(`/loans/${loan.value.loan_id}/returned`);
    alert('Sikeres visszavitel!');
    fetchLoan();
  } catch (error) {
    alert(error.response?.data?.message || 'Nem sikerült a visszavitel.');
  }
};

async function extendLoan() {
  try {
    await apiClient.post(`/loans/${loan.value.loan_id}/extend`);
    alert('Sikeres hosszabbítás!');
    fetchLoan();
  } catch (error) {
    alert(error.response?.data?.message || 'Nem sikerült a hosszabbítás.');
  }
};

async function finePaid() {
  try {
    await apiClient.post(`/loans/${loan.value.loan_id}/fine_paid`);
    alert('Sikeres fizetés!');
    fetchLoan();
  } catch (error) {
    alert(error.response?.data?.message || 'Nem sikerült a fizetés.');
  }
};

</script>

<template>
  <div v-if="loan">
    <h1>Kölcsönzés részletei</h1>
    <p><strong>Kölcsönzés ID:</strong> {{ loan.loan_id }}</p>
    <p><strong>Cím:</strong> {{ loan.book.title }}</p>
    <p><strong>Szerző:</strong> {{ loan.book.author }}</p>
    <p><strong>Kezdés dátuma:</strong> {{ loan.start_date }}</p>
    <p><strong>Határidő:</strong> {{ loan.due_date }}</p>
    <p><strong>Hosszabbítások száma:</strong> {{ loan.extension_count }}</p>
    <p v-if="loan.return_date"><strong>Visszahozva:</strong> {{ loan.return_date }}</p>
    <p><strong>Hosszabbítások száma:</strong> {{ loan.extension_count }} / 2</p>
    <strong>
      <p v-if="loan.overdue_fine" class="fine">Büntetés: {{ loan.overdue_fine }} Ft</p>
    </strong>
    <div v-if="authStore.user.role === 'librarian'" class="button-container">
      <button @click="extendLoan()" :disabled="loan.return_date || loan.extension_count >= 2">
        Hosszabbítás
      </button>

      <button @click="returnBook()" :disabled="loan.return_date" style="margin-left: 10px;">
        Visszahozatal
      </button>

      <button @click="finePaid()" :disabled="!loan.overdue_fine" style="margin-left: 10px;">
        Büntetés fizetve
      </button>
    </div>
  </div>
  <p v-else>Betöltés...</p>
</template>


<style>
.button-container {
  display: flex;
  gap: 4px;
}

.fine {
  color: red;
}

</style>
