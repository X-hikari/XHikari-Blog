<template>
  <div class="photo-list-container">
    <!-- 图片网格布局 -->
    <div class="photo-grid">
      <div
        v-for="(img, index) in images"
        :key="index"
        class="photo-item"
        @click="showFullScreen(index)"
      >
        <img
          :src="`http://localhost:8001${img}`"
          class="photo-img"
          :alt="'photo ' + index"
        />
      </div>
    </div>

    <!-- 全屏模式 -->
    <div v-if="isFullScreen" class="full-screen" @click="closeFullScreen">
      <img
        :src="`http://localhost:8001${images[currentIndex]}`"
        class="full-screen-img"
        :alt="'full photo ' + currentIndex"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  images: {
    type: Array,
    default: () => []
  },
  albumName: {
    type: String,
    required: true
  }
});

// 控制全图模式
const isFullScreen = ref(false);
const currentIndex = ref(0);

// 进入全屏模式
const showFullScreen = (index) => {
  currentIndex.value = index;  // 当前显示图片索引
  isFullScreen.value = true;    // 显示全屏模式
};

// 退出全屏模式
const closeFullScreen = () => {
  isFullScreen.value = false;   // 隐藏全屏模式
};
</script>

<style scoped>
.photo-list-container {
  width: 80%;
  text-align: center;
  margin: 0 auto;
  user-select: none;
}

/* 图片网格布局，每行最多四张图片 */
.photo-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 每行4张图片 */
  gap: 10px;
  margin-bottom: 20px;
}

.photo-item {
  cursor: pointer;
  overflow: hidden;
  border-radius: 10px;
}

.photo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
  transition: transform 0.3s ease;
}

.photo-item:hover .photo-img {
  transform: scale(1.1);  /* 鼠标悬停时放大 */
}

/* 全屏模式样式 */
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
