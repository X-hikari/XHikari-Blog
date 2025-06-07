import { createApp } from 'vue';
import AdminApp from './AdminApp.vue';
import { API_BASE_URL } from './config'
// import adminRouter from './router/admin';

const app = createApp(AdminApp)
// app.use(adminRouter)
app.mount("#admin-app")

  