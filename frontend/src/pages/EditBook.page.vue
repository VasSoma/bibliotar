<script setup>
import { apiClient } from '@/api-client/api.client'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

// lekerjuk apirol es berakjuk a formba

const route = useRoute()
const bookId = route.params.id
const isEdit = !!bookId

const author = ref('')
const isAvailable = ref(true)
const isbn = ref('')
const quantity = ref(0)
const title = ref('')

onMounted(async () => {
    const response = await apiClient.get(`/books/${bookId}`)
    author.value = response.data.author
    isAvailable.value = response.data.is_available
    isbn.value = response.data.isbn
    quantity.value = response.data.quantity
    title.value = response.data.title
})

async function onSubmit() {
    // post requesthez body
    const payload = {
        author: author.value,
        is_available: isAvailable.value,
        isbn: isbn.value,
        quantity: quantity.value,
        title: title.value,
    }

    if (isEdit) {
        await apiClient.patch(`/books/update`, { ...payload, id: bookId })
    }
    else {
        await apiClient.post(`/books/new`, payload)
    }
}

</script>

<template>
    <h1>{{ isEdit ? 'Konyv modositasa' : 'Uj konyv hozzaadasa' }}</h1>
    <form @submit.prevent="onSubmit" class="form">
        <input v-model="title" placeholder="Title" type="text" />
        <input v-model="author" placeholder="Author" type="text" />
        <input v-model="isbn" placeholder="ISBN" type="text" />
        <input v-model.number="quantity" placeholder="Quantity" type="number" />
        <label>
            <input v-model="isAvailable" type="checkbox" />
            Available
        </label>
        <button type="submit">{{ isEdit ? 'Save' : 'Add' }}</button>
        <p v-if="apiResponse">{{ apiResponse }}</p>
    </form>
</template>


<style scoped>
.form {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    max-width: 400px;
}
</style>