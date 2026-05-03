import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { setupApiClient } from '@/api-client/interceptors'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'

const app = createApp(App)
app.use(createPinia())

setupApiClient()

const auth = useAuthStore()
await auth.fetchUser()

app.use(router)
app.mount('#app')