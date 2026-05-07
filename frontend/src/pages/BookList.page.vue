<template>
  <div>
    <h1>Könyvkatalógus</h1>
    <div class="search-container">
      Kereses: <input type="text" v-model="search" @input="fetchBooks()" />
    </div>
    <div v-if="loading">Betöltés...</div>
    <div v-else-if="books.length">
      <!-- A backend a listában 'book_id' néven adja az azonosítót -->
      <div v-for="book in books" :key="book.book_id" @click="() => router.push(`/books/${book.book_id}`)"
        style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;">
        <h3>{{ book.title }}</h3>
        <p>Szerző: {{ book.author }}</p>
        <p>Mennyiség: {{ book.quantity }}</p>

      </div>
    </div>
    <p v-else>Nincs talalat a konyvekre</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { apiClient } from '../api-client/api.client';
import { useRouter } from 'vue-router';

const router = useRouter()
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

<style>
.search-container {
  margin: 12px 0;
}
</style>
