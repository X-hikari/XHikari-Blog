<template>
  <div class="container">
    <!-- 控制按钮列表 -->
    <div class="button-list">
      <button @click="currentView = adminMessage">信息管理</button>
      <button @click="currentView = adminArticle">文章管理</button>
    </div>

    <!-- 动态组件显示 -->
    <div class="component-display">
      <component :is="currentView" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import adminMessage from './adminPage/views/adminmessage/adminMessage.vue';
import adminArticle from './adminPage/views/adminArticle.vue';

const currentView = ref(adminMessage);
</script>

<style scoped>
* {
  box-sizing: border-box; /* 确保内边距和边框包含在宽度内 */
}

.container {
  display: flex;
  width: 100vw;
}

.button-list {
  width: 15%;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px;
  background-color: #f4f4f4;
}

.button-list button {
  padding: 10px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.button-list button:hover {
  background-color: #0056b3;
}

.component-display {
  flex: 1;
  padding: 20px;
  margin: 0 auto;
  max-width: 80%;
  width: 100%;
}
</style>
