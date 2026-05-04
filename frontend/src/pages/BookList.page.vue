<template>
  <div>
    <h1>Könyvkatalógus</h1>
    <div v-if="loading">Betöltés...</div>
    <div v-else>
      <!-- A backend a listában 'book_id' néven adja az azonosítót -->
      <div v-for="book in books" :key="book.book_id" style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;">
        <h3>{{ book.title }}</h3>
        <p>Szerző: {{ book.author }}</p>
        <p>Mennyiség: {{ book.quantity }}</p>
        
        <button 
          @click="rentBook(book.book_id)" 
          :disabled="!book.is_available || !authStore.isAuthenticated">
          Kölcsönzés
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { apiClient } from '../api-client/api.client';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const books = ref([]);
const loading = ref(false);

const fetchBooks = async () => {
  loading.value = true;
  try {
    const res = await apiClient.get('/books/');
    books.value = res.data;
  } catch (error) {
    console.error('Hiba a könyvek betöltésekor:', error);
  } finally {
    loading.value = false;
  }
};

const rentBook = async (bookId) => {
  console.log('--- Kölcsönzés indítása ---');
  console.log('Mentett UserID:', authStore.userId, 'Típusa:', typeof authStore.userId);
  console.log('Könyv ID:', bookId);

  if (!authStore.userId || isNaN(authStore.userId)) {
    alert("Hiba: Érvénytelen felhasználói azonosító! Kérlek, jelentkezz be újra.");
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
    console.error('Szerver hiba:', error.response?.data);
    alert('Hiba: ' + (error.response?.data?.message || 'Sikertelen tranzakció'));
  }
};

onMounted(fetchBooks);
</script>