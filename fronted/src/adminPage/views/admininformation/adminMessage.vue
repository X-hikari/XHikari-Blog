<template>
  <div>
    <!-- 控制按钮 -->
    <div class="button-container">
      <button 
        :class="{ active: currentView === Webmaster }" 
        @click="currentView = WebmasterComponent"
      >
        博主信息
      </button>
      <button 
        :class="{ active: currentView === WebInformation }" 
        @click="currentView = WebInformationComponent"
      >
        网站信息
      </button>
    </div>
  
    <!-- 动态组件显示 -->
    <component :is="currentView" />
  </div>
</template>

<script setup>
import { ref, markRaw } from 'vue';
import Webmaster from './Webmaster.vue';
import WebInformation from './WebInformation.vue';

const WebmasterComponent = markRaw(Webmaster)
const WebInformationComponent = markRaw(WebInformation)

const currentView = ref(Webmaster);
</script>

<style scoped>
/* 按钮容器样式 */
.button-container {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

/* 基础按钮样式 */
button {
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  border: 2px solid #007bff; /* 默认边框颜色 */
  border-radius: 5px;
  background-color: white;
  color: #007bff;
  cursor: pointer;
  transition: all 0.3s ease; /* 平滑过渡效果 */
}

/* 鼠标悬停样式 */
button:hover {
  background-color: #007bff;
  color: white;
  transform: scale(1.05); /* 放大效果 */
  box-shadow: 0px 4px 10px rgba(0, 123, 255, 0.3); /* 阴影效果 */
}

/* 激活状态样式 */
button.active {
  background-color: #007bff;
  color: white;
  box-shadow: 0px 4px 10px rgba(0, 123, 255, 0.5); /* 更明显的阴影 */
}

/* 点击时的效果 */
button:active {
  transform: scale(0.95); /* 缩小效果 */
}
</style>
