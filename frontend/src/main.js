import { createApp } from 'vue'
import App from './views/App.vue'
import router from './router' // Importa a config

createApp(App).use(router).mount('#app')