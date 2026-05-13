<script setup>
import { apiClient } from '@/api-client/api.client';
import { useAuthStore } from '@/stores/auth';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const loanId = route.params.id;
const loan = ref(null);
const authStore = useAuthStore();

onMounted(() => {
    fetchLoan();
});

async function fetchLoan() {
    try {
        const response = await apiClient.get(`/loans/${loanId}`);
        loan.value = response.data;
    } catch (error) {
        console.error('Kölcsönzés betöltési hiba:', error);
        alert('Nem sikerült betölteni a kölcsönzés adatait.');
    }
}

async function returnLoan() {
    if (!confirm('Biztosan visszaveszed ezt a könyvet?')) return;
    try {
        await apiClient.post(`/loans/${loanId}/returned`);
        alert('Könyv sikeresen visszavéve.');
        fetchLoan();
    } catch (error) {
        alert('Hiba: ' + (error.response?.data?.message || 'Visszavétel sikertelen.'));
    }
}

async function markFinePaid() {
    if (!confirm('Biztosan rendezettnek jelölöd a bírságot?')) return;
    try {
        await apiClient.post(`/loans/${loanId}/fine_paid`);
        alert('Bírság rendezése.');
        fetchLoan();
    } catch (error) {
        alert('Hiba: ' + (error.response?.data?.message || 'Bírság jelölés sikertelen.'));
    }
}

const formatDate = (dateStr) => {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleDateString('hu-HU');
};

const isReturnedLate = (loan) => {
    return new Date(loan.return_date) > new Date(loan.due_date);
};
</script>

<template>
    <div v-if="loan" class="booking-details">
        <h1>Kölcsönzés részletei</h1>

        <section>
            <h3>Könyv</h3>
            <p><strong>Cím:</strong> {{ loan.book?.title }}</p>
            <p><strong>Szerző:</strong> {{ loan.book?.author }}</p>
        </section>

        <section v-if="authStore.user?.role === 'librarian' || authStore.user?.role === 'admin'">
            <h3>Kölcsönző</h3>
            <p><strong>Név:</strong> {{ loan.user?.name }}</p>
            <p><strong>Email:</strong> {{ loan.user?.email }}</p>
        </section>

        <section>
            <h3>Kölcsönzés adatai</h3>
            <p><strong>Kezdet:</strong> {{ formatDate(loan.start_date) }}</p>
            <p><strong>Határidő:</strong> {{ formatDate(loan.due_date) }}</p>
            <p>
                <strong v-if="loan.return_date" :style="{ color: isReturnedLate(loan) ? 'red' : 'green', fontWeight: 'bold' }">Visszahozva: </strong>
                <span v-if="loan.return_date" :style="{ color: isReturnedLate(loan) ? 'red' : 'green', fontWeight: 'bold' }">
                    {{ formatDate(loan.return_date) }}
                </span>
                <span v-else>-</span>
            </p>
            <p><strong>Hosszabbítások:</strong> {{ loan.extension_count }}
                <span v-if="authStore.user?.role !== 'librarian'"> / 2</span>
            </p>
            <p v-if="loan.overdue_fine > 0" style="font-weight: bold;">
                <span v-if="loan.fine_is_paid" style="color: green;">
                    Bírság rendezve: <span style="color: red;">{{ loan.overdue_fine }}</span> Ft
                </span>
                <span v-else style="color: red;">
                    Büntetés: {{ loan.overdue_fine }} Ft
                </span>
            </p>
        </section>

        <div class="button-container" style="margin-top: 20px;">
            <button
                v-if="authStore.user?.role === 'librarian' && !loan.return_date"
                @click="returnLoan"
                style="background-color: #4caf50; color: white;">
                Könyv visszavétele
            </button>
            <button
                v-if="authStore.user?.role === 'librarian' && loan.overdue_fine > 0 && loan.return_date && !loan.fine_is_paid"
                @click="markFinePaid"
                style="background-color: #ff9800; color: white;">
                Bírság rendezése
            </button>
            <button @click="router.push('/bookings')">Vissza a listához</button>
        </div>
    </div>
    <p v-else>Betöltés...</p>
</template>

<style>
.booking-details section {
    margin-bottom: 16px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}
.button-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}
</style>
