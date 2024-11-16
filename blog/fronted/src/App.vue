<template>
  <div class="#app">
    <header class="header">
      <div class="header-content">
        <div class="left-actions">
          <div class="logo">
            <img src="@/assets/logo.svg" alt="Logo" />
          </div>
          <a href="#" class="login"><i class="iconfont icon-denglu-copy"></i> 登录</a>
          <button @click="toggleTheme">
            <i :class="isDarkMode ? 'icon-light-mode' : 'icon-dark-mode'"></i>
          </button>
        </div>
  
        <nav class="nav-links">
          <router-link to="/home"><i class="iconfont icon-zhuye"></i> 主页</router-link>
          <router-link to="/classify"><i class="iconfont icon-icon"></i> 分类</router-link>
          <router-link to="/photos"><i class="iconfont icon-xiangce"></i> 相册</router-link>
          <router-link to="/emotion"><i class="iconfont icon-comiisfashuoshuo"></i> 说说</router-link>
          <router-link to="/message"><i class="iconfont icon-liuyanban-05"></i> 留言</router-link>
          <router-link to="/more"><i class="iconfont icon-gengduo"></i> 更多</router-link>
          <router-link to="/music"><i class="iconfont icon-icon-test"></i> 音乐</router-link>
          <router-link to="/" class="search-link">
            <i class="iconfont icon-sousuo"></i> 搜索
            <!-- 搜索框 -->
          </router-link>
          <input type="text" class="search-input" placeholder="搜索..." />
        </nav>
      </div>
    </header>

    <TimeWatch />

    <!-- 动态标题 -->
    <div v-if="showTitle" class="page-title">
      <div class="page-title-text">Xhikari's blog</div> 
    </div>
  
    <div class="main-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router'; // 引入 Vue Router 的 useRoute hook
import TimeWatch from '@/components/TimeWatch.vue';

const isDarkMode = ref(false);
const route = useRoute(); // 获取当前路由对象
const showTitle = ref(false); // 用于控制标题显示

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value;
  document.body.classList.toggle('dark-mode', isDarkMode.value);
};

onMounted(() => {
  // 初始化时根据当前主题设置
  if (document.body.classList.contains('dark-mode')) {
    isDarkMode.value = true;
  }
});

watch(route, (newRoute) => {
  // 每次路由变化时，更新背景图显示的状态
  if (newRoute.path === '/home') {
    document.querySelector('.main-content').classList.add('no-background');
    showTitle.value = false; // 在首页不显示标题
  } else {
    document.querySelector('.main-content').classList.remove('no-background');
    showTitle.value = true; // 非首页显示标题
  }
});
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
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
  height: 30%;
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

</style>
