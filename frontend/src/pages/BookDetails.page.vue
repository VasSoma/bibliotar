
<script setup>
import { apiClient } from '@/api-client/api.client';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

    //books/:id
    //kivesszuk az id-t az URLbol
    const route = useRoute()
    const router = useRouter()
    const bookId = route.params.id 
    const book = ref(null)
    //meghivjuk azt a fvt ami a komponens letrejovetelekor fut le 
    //a fvben lekerjuk apirol az adott bookid-u bookot
    onMounted(async () => {
       const response = await apiClient.get(`/books/${bookId}`)
       book.value = response.data
    })

    async function onHandleEdit(){
        router.push(`/books/${bookId}/edit`)
    }

    async function onHandleDelete(){
       await apiClient.delete(`/books/${bookId}`)
       router.push('/books')
    }


</script>


<template>
  <div v-if="book">
    <h1>Könyv részletei</h1>
    <p><strong>ID:</strong> {{ book.id }}</p>
    <p><strong>Cím:</strong> {{ book.title }}</p>
    <p><strong>Szerző:</strong> {{ book.author }}</p>
    <p><strong>ISBN:</strong> {{ book.isbn }}</p>
    <p><strong>Mennyiség:</strong> {{ book.quantity }}</p>
    <p><strong>Elérhető:</strong> {{ book.is_available ? 'Igen' : 'Nem' }}</p>
    <div class="button-container">
        <button @click="onHandleEdit">Szerkesztés</button>
        <button @click="onHandleDelete">Torles</button>

    </div>
  </div>
  <p v-else>Betöltés...</p>
</template>

<style>
.button-container {
    display: flex;
    gap: 4px;
}
</style>