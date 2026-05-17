<script setup>
import { apiClient } from '@/api-client/api.client'
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const bookId = route.params.id
const isEdit = !!bookId

const author = ref('')
const isAvailable = ref(true)
const isbn = ref('')
const quantity = ref(0)
const title = ref('')

onMounted(async () => {
    if (!isEdit) return
    try {
        const response = await apiClient.get(`/books/${bookId}`)
        author.value = response.data.author
        isAvailable.value = response.data.is_available
        isbn.value = response.data.isbn
        quantity.value = response.data.quantity
        title.value = response.data.title
    } catch {
        alert('Nem sikerült betölteni a könyv adatait.')
        router.push('/books')
    }
})

async function onSubmit() {
    const payload = {
        author: author.value,
        is_available: isAvailable.value,
        isbn: isbn.value,
        quantity: quantity.value,
        title: title.value,
    }

    try {
        if (isEdit) {
            await apiClient.patch(`/books/${bookId}`, payload)
            alert('A könyv módosítása sikeres.')
        } else {
            await apiClient.post('/books', payload)
            alert('A könyv sikeresen hozzáadva.')
        }
        router.push('/books')
    } catch (error) {
        alert('Hiba: ' + (error.response?.data?.message || 'Sikertelen művelet.'))
    }
}
</script>

<template>
    <h1>{{ isEdit ? 'Könyv módosítása' : 'Új könyv hozzáadása' }}</h1>
    <form @submit.prevent="onSubmit" class="form">
        <label>
            Cím
            <input v-model="title" placeholder="Cím" type="text" required />
        </label>
        <label>
            Szerző
            <input v-model="author" placeholder="Szerző" type="text" required />
        </label>
        <label>
            ISBN
            <input v-model="isbn" placeholder="ISBN" type="text" required />
        </label>
        <label>
            Darabszám
            <input v-model.number="quantity" placeholder="Darabszám" type="number" min="0" required />
        </label>
        <label class="checkbox-label">
            <input v-model="isAvailable" type="checkbox" />
            Kölcsönözhető
        </label>
        <div class="button-row">
            <button type="submit">{{ isEdit ? 'Mentés' : 'Hozzáadás' }}</button>
            <button type="button" @click="router.push('/books')">Mégse</button>
        </div>
    </form>
</template>

<style scoped>
.form {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    max-width: 400px;
}
.form label {
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-weight: 500;
}
.checkbox-label {
    flex-direction: row !important;
    align-items: center;
    gap: 8px !important;
}
.button-row {
    display: flex;
    gap: 8px;
    margin-top: 8px;
}
</style>
