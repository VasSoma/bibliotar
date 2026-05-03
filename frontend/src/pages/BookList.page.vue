<template>
  <div>
    <h2>Kölcsönzések listája</h2>
    <p v-if="error" class="error">{{ error }}</p>
    
    <table class="table" v-if="loans.length > 0">
      <thead>
        <tr>
          <th>Könyv címe</th>
          <th>Kezdés</th>
          <th>Lejárat</th>
          <th>Műveletek</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="loan in loans" :key="loan.loan_id">
          <td>{{ loan.book.title }}</td>
          <td>{{ new Date(loan.start_date).toLocaleDateString() }}</td>
          <td>{{ new Date(loan.due_date).toLocaleDateString() }}</td>
          <td>
            <button v-if="!authStore.isLibrarian" @click="extendLoan(loan.loan_id)">Hosszabbítás</button>
            <template v-if="authStore.isLibrarian">
              <button @click="returnLoan(loan.loan_id)">Visszavétel</button>
              <button class="fine-btn" @click="payFine(loan.loan_id)">Bírság igazolása</button>
            </template>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>Nincsenek aktív kölcsönzések.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const loans = ref([])
const error = ref('')

const fetchLoans = async () => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/api/loans/history/${authStore.user_id}`, {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.message || 'Hiba a lekérdezésnél')
    loans.value = data
  } catch (err) {
    error.value = err.message
  }
}

const extendLoan = async (loanId) => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/api/loans/history/${loanId}/extend`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (!res.ok) throw new Error(await res.text())
    alert('Sikeres hosszabbítás!')
    fetchLoans()
  } catch (err) {
    alert("Hiba: " + err.message)
  }
}

const returnLoan = async (loanId) => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/api/loans/history/${loanId}/returned`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (!res.ok) throw new Error(await res.text())
    alert('Könyv visszavéve!')
    fetchLoans()
  } catch (err) {
    alert("Hiba: " + err.message)
  }
}

const payFine = async (loanId) => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/api/loans/history/${loanId}/fine_paid`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (!res.ok) throw new Error(await res.text())
    alert('Bírság befizetve!')
    fetchLoans()
  } catch (err) {
    alert("Hiba: " + err.message)
  }
}

onMounted(() => fetchLoans())
</script>

<style scoped>
.table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
.table th, .table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
.table th { background-color: #f2f2f2; }
button { padding: 0.5rem; cursor: pointer; background: #008CBA; color: white; border: none; border-radius: 3px; margin-right: 5px; }
.fine-btn { background: #ff9800; }
.error { color: red; }
</style>