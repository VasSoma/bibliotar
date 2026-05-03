<template>
  <div>
    <h1>Könyvkatalógus</h1>
    
    <input 
      v-model="searchQuery" 
      type="text" 
      placeholder="Keresés cím vagy szerző alapján..." 
    />

    <div>
      <div v-for="book in filteredBooks" :key="book.id">
        <h3>{{ book.title }}</h3>
        <p><strong>Szerző:</strong> {{ book.author }}</p>
        <p><strong>ISBN:</strong> {{ book.isbn }}</p>
        <p><strong>Elérhető példány:</strong> {{ book.quantity }}</p>
        <p v-if="!book.is_available">Jelenleg nem kölcsönözhető</p>

        <button 
          @click="reserveBook(book.id)" 
          :disabled="!book.is_available || !authStore.isAuthenticated">
          Előjegyzés
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { apiClient } from '../api-client/api.client';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const books = ref([]);
const searchQuery = ref('');

const fetchBooks = async () => {
  try {
    const res = await apiClient.get('/api/books/');
    books.value = res.data;
  } catch (error) {
    console.error('Könyvek betöltése sikertelen', error);
  }
};

const filteredBooks = computed(() => {
  if (!searchQuery.value) return books.value;
  const lowerCaseQuery = searchQuery.value.toLowerCase();
  return books.value.filter(b => 
    b.title.toLowerCase().includes(lowerCaseQuery) || 
    b.author.toLowerCase().includes(lowerCaseQuery)
  );
});

const reserveBook = async (bookId) => {
  try {
    await apiClient.post(`/api/loans/reserve`, { book_id: bookId });
    alert('Könyv sikeresen előjegyezve!');
    fetchBooks();
  } catch (error) {
    alert('Backend még nincs bruhuhu fehérvári fc');
  }
};

onMounted(() => {
  fetchBooks();
});
</script>