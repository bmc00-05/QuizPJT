import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import './assets/main.css'
import "./styles.css"
import "./styles/fonts.css"

import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
window.__BASE_URL__ = import.meta.env.BASE_URL
console.log('BASE_URL=', window.__BASE_URL__)
const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)

app.mount('#app')
