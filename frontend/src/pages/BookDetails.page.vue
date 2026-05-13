<script setup>
import { apiClient } from '@/api-client/api.client';
import { useAuthStore } from '@/stores/auth';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute()
const router = useRouter()
const bookId = route.params.id
const book = ref(null)
const targetUserEmail = ref('')
const authStore = useAuthStore()

onMounted(async () => {
    fetchBook()
})

async function onHandleEdit() {
    router.push(`/books/${bookId}/edit`)
}

async function onHandleDelete() {
    if (confirm("Biztosan törölni szeretnéd ezt a könyvet?")) {
        try {
            await apiClient.delete(`/books/${bookId}`)
            alert('A könyv sikeresen törölve.')
            router.push('/books')
        } catch (error) {
            console.error('Szerver oldali törlési hiba:', error);
            alert("Hiba történt a törlés során! \nValószínűleg a könyvhöz már tartozik kölcsönzés az adatbázisban, ezért nem törölhető.");
        }
    }
}

async function fetchBook() {
    try {
        const response = await apiClient.get(`/books/${bookId}`)
        book.value = response.data
    } catch (error) {
        console.error('Könyv betöltési hiba:', error);
        alert('Nem sikerült betölteni a könyv adatait.');
    }
}

async function rentBookAsUser() {
    try {
        await apiClient.post('/loans', {
            book_id: Number(bookId),
            user_id: authStore.user?.user_id
        });
        alert('Sikeres kölcsönzés!');
        fetchBook();
    } catch (error) {
        console.error('Szerver hiba:', error.response?.data);
        alert('Hiba: ' + (error.response?.data?.message || 'Sikertelen tranzakció'));
    }
}

async function rentBookAsLibrarian() {
    if (!targetUserEmail.value) {
        alert('Hiba: Adj meg egy email címet!');
        return;
    }
    try {
        await apiClient.post('/loans', {
            book_id: Number(bookId),
            user_email: targetUserEmail.value
        });
        alert('Sikeres kiadás!');
        fetchBook();
        targetUserEmail.value = '';
    } catch (error) {
        console.error('Szerver hiba:', error.response?.data);
        alert('Hiba: ' + (error.response?.data?.message || 'Sikertelen tranzakció'));
    }
}
</script>

<template>
    <div v-if="book" class="book-details">
        <h1>Könyv részletei</h1>
        <p><strong>ID:</strong> {{ book.book_id || book.id }}</p>
        <p><strong>Cím:</strong> {{ book.title }}</p>
        <p><strong>Szerző:</strong> {{ book.author }}</p>
        <p><strong>ISBN:</strong> {{ book.isbn }}</p>
        <p><strong>Mennyiség:</strong> {{ book.quantity }}</p>
        <p><strong>Elérhető:</strong> {{ book.is_available ? 'Igen' : 'Nem' }}</p>
        
        <div class="button-container" style="margin-top: 20px;">
            <button v-if="authStore.user?.role === 'admin'" @click="onHandleEdit">Szerkesztés</button>
            <button v-if="authStore.user?.role === 'admin'" @click="onHandleDelete" style="background-color: #ff4d4d; color: white;">Törlés</button>
            
            <button
                v-if="authStore.user?.role === 'user'"
                @click="rentBookAsUser"
                :disabled="!book.is_available || !authStore.isAuthenticated">
                Kölcsönzés
            </button>

            <div v-if="authStore.user?.role === 'librarian'" class="librarian-section" style="border: 1px solid #ccc; padding: 10px; margin-top: 10px;">
                <h4>Könyvtárosi kiadás</h4>
                <input
                    v-model="targetUserEmail"
                    type="email"
                    placeholder="Felhasználó email címe"
                    style="margin-right: 10px; width: 250px;"
                />
                <button
                    @click="rentBookAsLibrarian"
                    :disabled="!book.is_available || !targetUserEmail">
                    Kiadás felhasználónak
                </button>
            </div>
        </div>
    </div>
    <p v-else>Betöltés...</p>
</template>

<style>
.button-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}
</style>