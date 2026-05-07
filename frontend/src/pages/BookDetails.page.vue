<script setup>
import { apiClient } from '@/api-client/api.client';
import { useAuthStore } from '@/stores/auth';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

//books/:id
//kivesszuk az id-t az URLbol
const route = useRoute()
const router = useRouter()
const bookId = route.params.id
const book = ref(null)

// user es isAuthenticated flag eleresere
const authStore = useAuthStore()

//meghivjuk azt a fvt ami a komponens letrejovetelekor fut le 
//a fvben lekerjuk apirol az adott bookid-u bookot
onMounted(async () => {
    fetchBook()
})

async function onHandleEdit() {
    router.push(`/books/${bookId}/edit`)
}

async function onHandleDelete() {
    await apiClient.delete(`/books/${bookId}`)
    router.push('/books')
}


async function fetchBook() {
    const response = await apiClient.get(`/books/${bookId}`)
    book.value = response.data
}


async function rentBook() {
    console.log('--- Kölcsönzés indítása ---');
    console.log('Mentett UserID:', authStore.user?.user_id, 'Típusa:', typeof authStore.user?.user_id);
    console.log('Könyv ID:', book.value.book_id);

    if (!authStore.user?.user_id || isNaN(authStore.user?.user_id)) {
        alert("Hiba: Érvénytelen felhasználói azonosító! Kérlek, jelentkezz be újra.");
        return;
    }

    try {
        await apiClient.post('/loans', {
            book_id: Number(bookId),
            user_id: Number(authStore.user?.user_id)
        });
        alert('Sikeres kölcsönzés!');
        fetchBook();
    } catch (error) {
        console.error('Szerver hiba:', error.response?.data);
        alert('Hiba: ' + (error.response?.data?.message || 'Sikertelen tranzakció'));
    }

};


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
            <button v-if="authStore.user?.role === 'admin' " @click="onHandleEdit">Szerkesztés</button>
            <button v-if="authStore.user?.role === 'admin' " @click="onHandleDelete">Torles</button>
            <button v-if="authStore.user?.role === 'user' " @click="rentBook(book.book_id)" :disabled="!book.is_available || !authStore.isAuthenticated">
                Kölcsönzés
            </button>
        </div>
    </div>
    <p v-else>Betöltés...</p>
</template>0

<style>
.button-container {
    display: flex;
    gap: 4px;
}
</style>
