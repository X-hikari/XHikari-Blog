import './assets/main.css'
import './assets/css/global.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index'
import '@/assets/icons/iconfont/iconfont.css' 
import { createPinia } from 'pinia';
import { API_BASE_URL } from './config'

const app = createApp(App)

app.use(router)
app.use(createPinia());

// if (process.env.NODE_ENV === 'development') {
//     import('vue').then(vue => {
//         vue.default.config.devtools = true;
//     });
// } else {
//     app.config.devtools = false;
// }

app.mount('#app')
