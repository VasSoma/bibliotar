<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import {apiClient} from '@/api-client/api.client'

const route = useRoute()
const loanId = route.params.id
const loan = ref(null)

onMounted(async () => {
  const { data } = await apiClient.get(`/loans/history/${loanId}`)
  loan.value = data
})
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
  </div>
  <p v-else>Betöltés...</p>
</template>