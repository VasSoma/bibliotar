<script setup>
import { ref } from 'vue'
import axios from 'axios'
const books = ref([])

const getBooks = async () => {
  const response = await axios.get('https://potterapi-fedeperin.vercel.app/en/books')
  books.value = response.data
}

getBooks()
</script>

<template>
  <div>
    <div v-for="book in books" :key="book.number" class="list">
      <p>{{book.number}}</p>
      <p>{{book.title}}</p>
      <p>{{book.releaseDate}}</p>
    </div>
  </div>
</template>

<style scoped>
.list{display: grid;gap: 20px; grid-template-columns:50px 200px 100px}
</style>
