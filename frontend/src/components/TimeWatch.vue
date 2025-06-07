<template>
  <div class="image-container" @mouseenter="isOverlayVisible = true" @mouseleave="isOverlayVisible = false">
    <!-- 小的图片 -->
    <img src="/PocketWatch.svg" alt="Pocket Watch" class="pocket-watch" />

    <!-- 鼠标悬停时显示的透明矩形框 -->
    <div v-show="isOverlayVisible" class="overlay">
      <span class="current-time">
        嘟嘟噜~ 当前时间
        <span class="time">{{ currentTime }}</span>
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isOverlayVisible = ref(false);
const currentTime = ref('');

// 更新当前时间
const updateCurrentTime = () => {
  const now = new Date();
  currentTime.value = now.toLocaleTimeString();
};

// 定时每秒更新一次时间
let timer;
onMounted(() => {
  updateCurrentTime();
  timer = setInterval(updateCurrentTime, 1000);
});

onUnmounted(() => {
  clearInterval(timer);
});
</script>

<style scoped>
/* 图片容器样式 */
.image-container {
  position: fixed;
  top: 30%;
  right: 0;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  cursor: pointer;
  z-index: 1000;
}

/* 图片样式（小图片） */
.pocket-watch {
  width: 80px;  /* 调整图片大小 */
  height: 80px;
  object-fit: cover;
  border-radius: 50%;
  margin-left: 10px;  /* 留出空间给透明框 */
}

/* 透明矩形框样式 */
.overlay {
  position: absolute;
  top: 50%;
  right: 100%; /* 将透明框定位到图片的左边 */
  transform: translateY(-50%); /* 高度平齐 */
  width: auto;  /* 设置框的宽度 */
  padding: 5px 10px;
  background-color: rgba(0, 0, 0, 0.5); /* 半透明黑色背景 */
  border-radius: 8px;  /* 圆角矩形 */
  color: white;
  font-size: 1.2em;
  text-align: center;
  white-space: nowrap; /* 防止文字换行 */
}

/* 当前时间样式 */
.current-time {
  font-weight: bold;
}

.time {
  display: block;  /* 强制换行 */
  margin-top: 5px; /* 给时间和文本之间加点间距 */
}
</style>
