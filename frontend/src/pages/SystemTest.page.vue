<template>
  <div style="max-width: 850px; margin: 0 auto; font-family: monospace; padding-bottom: 50px;">
    <h1> Okos Sztori Teszt (Brutál Hibalogokkal)</h1>
    <div style="display: flex; gap: 15px; margin-bottom: 20px;">
      <div class="account-box">
        <h3>User</h3>
        <input v-model="accounts.user.email" class="input-field" placeholder="Email" /><br>
        <input v-model="accounts.user.password" type="password" class="input-field" placeholder="Jelszó" />
      </div>
      <div class="account-box">
        <h3>Könyvtáros</h3>
        <input v-model="accounts.librarian.email" class="input-field" placeholder="Email" /><br>
        <input v-model="accounts.librarian.password" type="password" class="input-field" placeholder="Jelszó" />
      </div>
      <div class="account-box">
        <h3>Admin</h3>
        <input v-model="accounts.admin.email" class="input-field" placeholder="Email" /><br>
        <input v-model="accounts.admin.password" type="password" class="input-field" placeholder="Jelszó" />
      </div>
    </div>

    <button @click="runStory" :disabled="isRunning" style="width: 100%; padding: 15px; font-size: 16px; font-weight: bold; background: #e67e22; color: white; border: none; cursor: pointer; border-radius: 5px;">
      {{ isRunning ? 'Sztori folyamatban...' : 'AKCIÓ:TESZT INDÍTÁSA' }}
    </button>

    <div style="margin-top: 20px; background: #111; color: #0f0; padding: 15px; border-radius: 5px; min-height: 400px; overflow-y: auto; border: 2px solid #333; white-space: pre-wrap;">
      <div v-for="(log, index) in logs" :key="index" :style="{ color: log.color, marginBottom: '8px', fontWeight: log.bold ? 'bold' : 'normal', wordWrap: 'break-word' }">
        {{ log.text }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { apiClient } from '../api-client/api.client';

const logs = ref([]);
const isRunning = ref(false);

const accounts = ref({
  user: { email: 'user@email.com', password: 'user' },
  librarian: { email: 'librarian@email.com', password: 'librarian' },
  admin: { email: 'admin@email.com', password: 'admin' }
});

const addLog = (msg, type = 'info') => {
  const colors = { info: '#ccc', success: '#0f0', error: '#ff5252', action: '#ffeb3b', title: '#00bcd4' };
  logs.value.push({ text: msg, color: colors[type], bold: type === 'title' || type === 'action' });
};

// EZ A VARÁZSFÜGGVÉNY: Kiszedi a pontos Network/CORS hibát
const getErrorDetails = (error) => {
  let reqInfo = "";
  if (error.config) {
    reqInfo = `\n Metódus: ${error.config.method?.toUpperCase()}`;
    reqInfo += `\n Végpont: ${error.config.baseURL || ''}${error.config.url}`;
    if (error.config.data) {
      reqInfo += `\n Payload: ${error.config.data}`;
    }
  }

  if (error.response) {
    return `[HTTP ${error.response.status} HIBA] \n Szerver válasza: ${JSON.stringify(error.response.data)}${reqInfo}`;
  } else if (error.request) {
    return `[HÁLÓZATI / CORS HIBA] A szerver blokkolt vagy nem válaszol! \n Belső hiba: ${error.message}${reqInfo}\n TIPP A BACKENDNEK: A frontend elküldte az adatot. Ellenőrizzétek a CORS-t és az OPTIONS kérést!`;
  } else {
    return `[KLIENS HIBA] \n Belső hiba: ${error.message}${reqInfo}`;
  }
};

const loginAs = async (roleKey) => {
  const acc = accounts.value[roleKey];
  const res = await apiClient.post('/auth/login', { email: acc.email, password: acc.password });
  localStorage.setItem('token', res.data.token);
  const profile = await apiClient.get('/user/profile');
  return profile.data;
};

const runStory = async () => {
  logs.value = [];
  isRunning.value = true;
  let activeBookId = null;
  let activeLoanId = null;

  addLog('===HIVATALOS DOKUMENTÁCIÓ TESZT ELINDULT ===', 'title');

  try {
    // ---------------------------------------------------------
    // 1. FELVONÁS: A SIMA USER
    // ---------------------------------------------------------
    addLog('\n[1. FELVONÁS: A USER AKCIÓBA LÉP]', 'action');
    let userProfile;
    try {
      userProfile = await loginAs('user');
      addLog(`User belépve. (Email: ${userProfile.email || accounts.value.user.email})`, 'info');
    } catch (e) {
      throw new Error(`Login hiba (User): ${getErrorDetails(e)}`);
    }

    try {
      await apiClient.patch('/user/profile', { phone_number: '+36301234567' });
      addLog(`✔ User: Személyes adatok sikeresen frissítve!`, 'success');
    } catch (e) {
      addLog(`❌ User adatfrissítés elhasalt!\n${getErrorDetails(e)}`, 'error');
    }

    let booksRes;
    try {
      booksRes = await apiClient.get('/books');
      const availableBook = booksRes.data.find(b => b.quantity > 0);
      if (!availableBook) throw new Error("Nincs a rendszerben kikölcsönözhető könyv!");
      activeBookId = availableBook.book_id || availableBook.id;
      addLog(`User böngészik: Talált egy szabad könyvet: "${availableBook.title}"`, 'info');
    } catch (e) {
      throw new Error(`Könyvlista lekérés hiba:\n${getErrorDetails(e)}`);
    }

    try {
      await apiClient.post('/loans/history/create', { book_id: activeBookId, user_id: userProfile.user_id || userProfile.id });
      addLog(`✔ User: Könyv sikeresen kikölcsönözve!`, 'success');
    } catch(e) {
      throw new Error(`Kölcsönzés hiba:\n${getErrorDetails(e)}`);
    }

    try {
      const loansRes = await apiClient.get('/loans');
      const myLoan = loansRes.data.find(l => (l.book_id === activeBookId || l.book?.book_id === activeBookId) && !l.return_date);
      activeLoanId = myLoan.loan_id;
    } catch(e) {
      throw new Error(`Nem találom a saját kölcsönzésemet:\n${getErrorDetails(e)}`);
    }

    try {
      await apiClient.post(`/loans/history/${activeLoanId}/extend`);
      addLog(`✔ User: 1. Hosszabbítás sikeres!`, 'success');
      await apiClient.post(`/loans/history/${activeLoanId}/extend`);
      addLog(`✔ User: 2. Hosszabbítás sikeres!`, 'success');
    } catch(e) {
      addLog(`❌ Hosszabbítás elhasalt a limithatár előtt!\n${getErrorDetails(e)}`, 'error');
    }

    try {
      await apiClient.post(`/loans/history/${activeLoanId}/extend`);
      addLog(`❌ HIBA: A backend engedte a 3. hosszabbítást a usernek! Ezt nem szabadna!`, 'error');
    } catch (e) {
      addLog(`✔ User: 3. Hosszabbítás elutasítva. (Helyes működés! Válasz: ${e.response?.status})`, 'success');
    }

    // ---------------------------------------------------------
    // 2. FELVONÁS: A KÖNYVTÁROS
    // ---------------------------------------------------------
    addLog('\n[2. FELVONÁS: A KÖNYVTÁROS BEAVATKOZIK]', 'action');
    try {
      await loginAs('librarian');
      addLog(`Könyvtáros belépve.`, 'info');
    } catch(e) {
      throw new Error(`Login hiba (Könyvtáros):\n${getErrorDetails(e)}`);
    }

    try {
      const anotherBook = booksRes.data.find(b => b.quantity > 0 && (b.book_id || b.id) !== activeBookId);
      if(anotherBook) {
        await apiClient.post('/loans/history/create', { book_id: anotherBook.book_id || anotherBook.id, user_email: accounts.value.user.email });
        addLog(`✔ Könyvtáros: Másik könyv sikeresen kiadva EMAIL alapján!`, 'success');
      } else {
        addLog(`⚠ Nincs elég szabad könyv a második kiadás teszteléséhez.`, 'info');
      }
    } catch(e) {
       addLog(`❌ Könyvtárosi kiadás (email alapján) elhasalt!\n${getErrorDetails(e)}`, 'error');
    }

    try {
      await apiClient.post(`/loans/history/${activeLoanId}/fine_paid`);
      addLog(`✔ Könyvtáros: Bírság befizetése regisztrálva!`, 'success');
    } catch (e) {
      addLog(`❌ Bírság kezelés elhasalt!\n${getErrorDetails(e)}`, 'error');
    }

    try {
      await apiClient.post(`/loans/history/${activeLoanId}/returned`);
      addLog(`✔ Könyvtáros: Könyv visszavétele sikeres!`, 'success');
    } catch (e) {
      addLog(`❌ Visszavétel elhasalt!\n${getErrorDetails(e)}`, 'error');
    }

    // ---------------------------------------------------------
    // 3. FELVONÁS: AZ ADMINISZTRÁTOR
    // ---------------------------------------------------------
    addLog('\n[3. FELVONÁS: AZ ADMINISZTRÁTOR DOLGOZIK]', 'action');
    try {
      await loginAs('admin');
      addLog(`Admin belépve.`, 'info');
    } catch(e) {
      throw new Error(`Login hiba (Admin):\n${getErrorDetails(e)}`);
    }

    let newBookId = null;

    try {
      const createRes = await apiClient.post('/books/new', { title: "BiblioTár Dokumentáció", author: "Rendszer Teszt", isbn: "999888777", quantity: 5, is_available: true });
      if (createRes.data && (createRes.data.book_id || createRes.data.id)) {
        newBookId = createRes.data.book_id || createRes.data.id;
      } else {
        const blist = await apiClient.get('/books');
        newBookId = blist.data[blist.data.length - 1].book_id;
      }
      addLog(`✔ Admin: Új könyv felvéve a rendszerbe!`, 'success');
    } catch (e) {
      addLog(`❌ Könyv felvétele elhasalt!\n${getErrorDetails(e)}`, 'error');
    }

    if (newBookId) {
      try {
        await apiClient.patch(`/books/${newBookId}`, { is_available: false, title: "BiblioTár (Sérült)" });
        addLog(`✔ Admin: Könyv állapota sikeresen módosítva!`, 'success');
      } catch (e) {
        addLog(`❌ Könyv állapot módosítása elhasalt!\n${getErrorDetails(e)}`, 'error');
      }

      try {
        await apiClient.delete(`/books/${newBookId}`);
        addLog(`✔ Admin: Könyv sikeresen törölve a rendszerből!`, 'success');
      } catch (e) {
        addLog(`❌ Könyv törlése elhasalt!\n${getErrorDetails(e)}`, 'error');
      }
    }

    addLog('\n===A TESZT SIKERESEN VÉGET ÉRT ===', 'title');

  } catch (error) {
    addLog(`\nKATASTRÓFA: A sztori megszakadt! Részletek:\n${error.message}`, 'error');
  } finally {
    localStorage.removeItem('token');
    isRunning.value = false;
  }
};
</script>

<style scoped>
.account-box {
  flex: 1;
  background: #2a2a2a;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #444;
  color: white;
}
.input-field {
  width: 90%;
  margin-bottom: 5px;
  padding: 5px;
  background: #444;
  color: white;
  border: 1px solid #666;
}
</style>