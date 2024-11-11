import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'; 

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/home' }, // 自动重定向到 /home
    { path: '/home', name: 'Home', component: Home },
  ],
})

export default router
