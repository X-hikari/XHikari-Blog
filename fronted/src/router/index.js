import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'; 
import Classify from '../views/Classify.vue'; 
import Article from '@/views/Article.vue';
import Category from '@/views/Category.vue';
import Album from '@/views/Album.vue';

const routes = [
  { path: '/', redirect: '/home' }, // 自动重定向到 /home
  { path: '/home', name: 'Home', component: Home },
  { path: '/classify', name: 'Classify', component: Classify },
  { path: '/category', name: 'Category', component: Category },
  { path: '/article', name: 'Article', component: Article },
  { path: '/album', name: 'Album', component: Album },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
  scrollBehavior(to, from, savedPosition) {
    // 每次页面切换时滚动到顶部
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  }
})

export default router
