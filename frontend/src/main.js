import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from '@/stores/auth'

import './api-client/interceptors'
import { setupApiClient } from './api-client/interceptors'

const app = createApp(App)
app.use(createPinia())

setupApiClient()

// try to fetch profile with token read from local storage
const auth = useAuthStore()
await auth.fetchUser()

app.use(router)
app.mount('#app')