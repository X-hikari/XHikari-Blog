<template>
  <div class="emotion-card">
    <div class="timestamp">
      <span class="date"><i class="iconfont icon-rili"></i> {{ formattedDate }}</span>
      <span class="divider">|</span>
      <span class="time"><i class="iconfont icon-shizhong"></i> {{ formattedTime }}</span>
    </div>
    <div v-if="text" class="text-content">{{ text }}</div>
    <div v-if="images.length" class="image-grid">
      <img v-for="(img, index) in images" 
      :key="index" 
      :src="`http://localhost:8001${img}`" 
      @click="showFullScreen(index)"
      class="image-item" />
    </div>
  </div>

  <!-- 大图显示 -->
  <div v-if="isFullScreen" class="full-screen" @click="closeFullScreen">
    <img
      :src="`http://localhost:8001${images[currentIndex]}`"
      class="full-screen-img"
      :alt="'full photo ' + currentIndex"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const currentIndex = ref(0);
const isFullScreen = ref(false);

const props = defineProps({
  text: String,
  created_at: String,
  images: Array
});

const formattedDate = computed(() => props.created_at?.split(' ')[0] || '');
const formattedTime = computed(() => props.created_at?.split(' ')[1] || '');

const showFullScreen = (index) => {
  currentIndex.value = index;  // 显示当前图片
  isFullScreen.value = true;    // 进入全屏模式
};

const closeFullScreen = () => {
  isFullScreen.value = false;   // 退出全屏模式
};
</script>

<style scoped>
.emotion-card {
  position: relative;
  width: 100%;
  background: rgba(255, 255, 255, 0.8) !important;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  word-wrap: break-word;
}

.timestamp {
  position: absolute;
  top: -8px;
  left: 0px;
  background: rgba(255, 255, 255, 1);
  color: rgb(0, 0, 0);
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 0.8em;
  display: flex;
  align-items: center;
  gap: 6px;
}

.divider {
  color: white;
  font-weight: bold;
}

.text-content {
  font-size: 1em;
  color: #333;
  margin-top: 24px;
  margin-bottom: 12px;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 8px;
}

.image-item {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
}

/* 全屏模式的样式 */
.full-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.full-screen-img {
  max-width: 90%;
  max-height: 90%;
  object-fit: contain;
  border-radius: 12px;
  cursor: pointer;
}
</style>
