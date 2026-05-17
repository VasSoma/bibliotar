<template>
  <div>
    <h1>Könyvkatalógus</h1>
    <div class="search-container">
      Keresés: <input type="text" v-model="search" @input="fetchBooks()" />
    </div>
    <button v-if="authStore.user?.role === 'admin'" class="btn-add" @click="router.push('/books/new')">
      + Új könyv hozzáadása
    </button>
    <div v-if="loading">Betöltés...</div>
    <div v-else-if="books.length">
      <div
        v-for="book in books"
        :key="book.book_id"
        class="book-card"
        @click="() => router.push(`/books/${book.book_id}`)"
      >
        <h3>{{ book.title }}</h3>
        <p><strong>Szerző:</strong> {{ book.author }}</p>
        <p><strong>Mennyiség:</strong> {{ book.quantity }}</p>
      </div>
    </div>
    <p v-else>Nincs találat a könyvekre</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { apiClient } from '../api-client/api.client';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter()
const authStore = useAuthStore()
const books = ref([]);
const loading = ref(false);
const search = ref("");

const fetchBooks = async () => {
  loading.value = true;
  try {
    const res = await apiClient.get(search.value ? `/books?search=${search.value}` : '/books');
    books.value = res.data;
  } catch (error) {
    console.error('Hiba a könyvek betöltésekor:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchBooks);
</script>

<style scoped>
.search-container {
  margin: 12px 0;
}

.btn-add {
  margin-bottom: 12px;
}

.book-card {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.15s;
}

.book-card:hover {
  background-color: #f5f5f5;
}

.book-card h3 {
  margin: 0 0 6px 0;
}

.book-card p {
  margin: 2px 0;
}
</style>
