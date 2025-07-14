<template>
  <div class="#app">
    <header class="header">
      <div class="header-content">
        <Login v-if="showLogin" @close="showLogin = false" />
        <div class="left-actions">
          <div class="logo">
            <img src="@/assets/logo.svg" alt="Logo" />
          </div>
          <a class="login" @click="login()"><i class="iconfont icon-denglu-copy"></i> 登录</a>
          <button @click="toggleTheme">
            <i :class="isDark ? 'icon-light-mode' : 'icon-dark-mode'"></i>
          </button>

          <!-- 汉堡按钮（仅在小屏显示） -->
          <div class="hamburger" @click="toggleMenu">
            <i class="iconfont icon-liebiao"></i>
          </div>
        </div>

        <nav v-show="menuOpen || isWideScreen" class="nav-links">
          <router-link to="/home"><i class="iconfont icon-zhuye"></i> 主页</router-link>
          <router-link to="/classify"><i class="iconfont icon-icon"></i> 分类</router-link>
          <router-link to="/album"><i class="iconfont icon-xiangce"></i> 相册</router-link>
          <router-link to="/emotion"><i class="iconfont icon-comiisfashuoshuo"></i> 说说</router-link>
          <router-link to="/message"><i class="iconfont icon-liuyanban-05"></i> 留言</router-link>
          <router-link to="/more"><i class="iconfont icon-gengduo"></i> 更多</router-link>
          <router-link :to="{ path: '/search', query: { q: searchQuery } }" @click="clearSearch" class="search-link">
            <i class="iconfont icon-sousuo"></i> 搜索
          </router-link>
          <!-- 搜索框 -->
          <input type="text" v-model="searchQuery" class="search-input" placeholder="搜索..." />
        </nav>
      </div>
    </header>

    <TimeWatch />

    <!-- 动态标题 -->
    <div v-if="showTitle" class="page-title">
      <div class="page-title-text">Xhikari's blog</div> 
    </div>
    
    <div>
      <MusicPlayer />
    </div>

    <div class="main-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import { useRoute } from 'vue-router'; // 引入 Vue Router 的 useRoute hook
import axios from 'axios';
import TimeWatch from '@/components/TimeWatch.vue';
import MusicPlayer from './components/Music/MusicPlayer.vue';
import Login from './components/Login.vue';

const isDark = ref(localStorage.getItem("theme") === "dark");
const route = useRoute(); // 获取当前路由对象
const showTitle = ref(false); // 用于控制标题显示
const searchQuery = ref(""); // 搜索框的绑定值
const showLogin = ref(false);
const menuOpen = ref(false);
const isWideScreen = ref(window.innerWidth > 768);

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value;
};

const handleResize = () => {
  isWideScreen.value = window.innerWidth > 768;
  if (isWideScreen.value) {
    menuOpen.value = false; // 自动关闭菜单
  }
};

const toggleTheme = () => {
  isDark.value = !isDark.value;
  document.documentElement.classList.toggle("dark-mode", isDark.value);
  localStorage.setItem("theme", isDark.value ? "dark" : "light");
};

const login = () => {
  showLogin.value = !showLogin.value;
}

watch(showLogin, (newValue) => {
  if (newValue) {
    document.body.style.overflow = "hidden"; // 禁止滚动
  } else {
    document.body.style.overflow = ""; // 恢复滚动
  }
});

const VisitUser = async () => {
  const response = await axios.post("http://localhost:8001/api/visit/");
  if (response.status == 200) {
    console.log("记录访问成功");
  }
}

onMounted(() => {
  VisitUser();
  // 初始化时根据当前主题设置
  if (document.body.classList.contains('dark-mode')) {
    isDark.value = true;
  }
  window.addEventListener('resize', handleResize);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
});

watch(route, (newRoute) => {
  if (newRoute.name === 'NotFound') {
    // 404 页面
    document.querySelector('.main-content').classList.add('no-background');
    showTitle.value = false;
    return ;
  }

  // 每次路由变化时，更新背景图显示的状态
  if (newRoute.path === '/home' || newRoute.path === '/message') {
    document.querySelector('.main-content').classList.add('no-background');
    showTitle.value = false; // 在首页不显示标题
  } else if (newRoute.path === '/album' || newRoute.path === '/photo') {
    document.querySelector('.main-content').classList.remove('no-background');
    showTitle.value = false;
  } else {
    document.querySelector('.main-content').classList.remove('no-background');
    showTitle.value = true; // 非首页显示标题
  }
});

const clearSearch = () => {
  searchQuery.value = ''; // 清空搜索框
}
</script>

<style scoped>
.header {
  width: 100%;
  background-color: #f8f8f8;
  opacity: 0.8;
  padding: 10px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;  
  top: 0;        
  left: 0;
  z-index: 1000;     /* 确保导航栏在其他内容之上 */
  user-select: none;
  outline: none !important;
}

.header-content {
  width: 100%;
  max-width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logo img {
  width: 30px;
  height: 30px;
  border-radius: 50%;
}

.nav-links {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  align-items: center;
}

.nav-links a {
  color: #333;
  text-decoration: none;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.nav-links a:hover {
  color: #007bff; 
}

.nav-links i {
  margin-right: 8px;
}

.search-link {
  display: flex;
  align-items: center;
  position: relative;
}

.search-input {
  margin-left: 8px;
  padding: 5px 10px;
  border-radius: 20px;
  border: 1px solid #ccc;
  background-color: transparent; /* 透明背景 */
  color: #333;
  outline: none;
  font-size: 14px;
  transition: border-color 0.3s;
}

.search-input::placeholder {
  color: #aaa; /* 占位符颜色 */
}

.search-input:focus {
  border-color: #007bff;
}

.icon-search {
  font-size: 20px;
}

.icon-home {
  font-size: 20px;
}

.icon-timeline {
  font-size: 20px;
}

.icon-category {
  font-size: 20px;
}

.icon-photo {
  font-size: 20px;
}

.icon-comments {
  font-size: 20px;
}

.icon-link {
  font-size: 20px;
}

.icon-message {
  font-size: 20px;
}

.actions {
  display: flex;
  gap: 15px;
  align-items: center;
}

.login {
  color: #333;
  text-decoration: none;
}

.login:hover {
  color: #007bff;
}

button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
}

.icon-light-mode::before {
  content: "🌞";
}

.icon-dark-mode::before {
  content: "🌙";
}

/* Dark mode styles */
.dark-mode {
  background-color: #333;
  opacity: 0.6;
  color: #f8f8f8;
}

.dark-mode .header {
  background-color: #444;
}

.dark-mode .login {
  color: white;
}

.dark-mode .nav-links a {
  color: white;
}

.dark-mode .login:hover {
  color: #007bff;
}

.dark-mode .nav-links a:hover {
  color: #007bff;
}

.dark-mode .search-input {
  color: white;
}

.main-content {
  position: relative;
  width: 100%;
  /* background-color: rgba(248, 248, 248, 0.8); */
  /* opacity: 0.8; */
  padding: 0;
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); */
  user-select: none;
}

.main-content::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/background.jpg');
  background-size: cover;
  background-position: center;
  z-index: -1;  /* 确保背景图在内容后面 */
  /* opacity: 0.8;  */
}

.main-content.no-background::before {
  display: none; /* 如果是首页，隐藏背景图 */
}

.page-title {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 580px;
  font-size: 2rem;
  text-align: center;
  padding: 10px;
}

.page-title .page-title-text {
  font-size: 48px;
  font-weight: bold;
  color: #8683e8;
  z-index: 1;
}

/* 通用响应式设置 */
.header-content,
.nav-links,
.left-actions {
  flex-wrap: wrap;
  flex-direction: row;
}

.nav-links {
  flex: 1 1 auto;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.search-input {
  max-width: 160px;
  width: 100%;
}

/* 汉堡按钮 */
.hamburger {
  display: none;
  font-size: 24px;
  cursor: pointer;
}

/* 过渡动画 */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@media screen and (max-width: 768px) {
  .hamburger {
    display: block;
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .left-actions {
    justify-content: space-between;
    width: 100%;
  }

  .nav-links {
    flex-direction: column;
    width: 100%;
    align-items: flex-start;
    gap: 6px;
    padding-top: 6px;
  }

  .nav-links a {
    width: 100%;
    padding: 6px 0;
  }

  .search-input {
    width: 100%;
    margin-left: 0;
    margin-top: 3px;
  }

  .page-title {
    height: auto;
    padding: 15px 10px;
    text-align: center;
  }

  .page-title .page-title-text {
    font-size: 24px;
  }
}

</style>
