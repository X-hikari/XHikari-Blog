<template>
  <div class="photo-container">
    <button @click="moveLeft" class="move-btn left-btn">
      <i class="iconfont icon-arrow-left-s-line" style="font-size: 30px;"></i>
    </button>
      
    <div class="photo-stack">
      <div
        v-for="(img, index) in images"
        :key="index"
        class="photo"
        :style="getTransform(index)"
        @click="showFullScreen(index)"
      >
        <img
          :src="`http://localhost:8001${img}`"
          class="photo-img"
          :alt="'photo ' + index"
        />
      </div>
    </div>

    <button @click="moveRight" class="move-btn right-btn">
      <i class="iconfont icon-arrow-right-s-line" style="font-size: 30px;"></i>
    </button>
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
import { ref } from 'vue';

const currentIndex = ref(0);
const isFullScreen = ref(false); // 新增的状态，用于控制大图模式

const props = defineProps({
  images: {
    type: Array,
    default: () => []
  },
  albumName: {
    type: String,
    required: true
  }
})

const moveLeft = () => {
  currentIndex.value = (currentIndex.value - 1 + props.images.length) % props.images.length;
};

const moveRight = () => {
  currentIndex.value = (currentIndex.value + 1) % props.images.length;
};

const showFullScreen = (index) => {
  currentIndex.value = index;  // 显示当前图片
  isFullScreen.value = true;    // 进入全屏模式
};

const closeFullScreen = () => {
  isFullScreen.value = false;   // 退出全屏模式
};

const getTransform = (index) => {
  const prevIndex = (currentIndex.value - 1 + props.images.length) % props.images.length;
  const nextIndex = (currentIndex.value + 1) % props.images.length;
  
  const baseStyle = {
    transition: 'transform 0.5s ease-out',
    zIndex: 1,
  };

  if (index === currentIndex.value) {
    return {
      ...baseStyle,
      transform: 'translateX(0) scale(1.2) rotateY(0deg)',
      zIndex: 3,
    };
  }
  
  if (index === prevIndex) {
    return {
      ...baseStyle,
      transform: 'translateX(-55%) rotateY(-30deg) scale(0.8)',
    };
  }
  
  if (index === nextIndex) {
    return {
      ...baseStyle,
      transform: 'translateX(55%) rotateY(30deg) scale(0.8)',
    };
  }

  return {
    ...baseStyle,
    transform: 'scale(0)',
    zIndex: 0,
  };
};
</script>

<style scoped>
.photo-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 500px;
}

.move-btn {
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  padding: 10px 10px;
  font-size: 28px;
  cursor: pointer;
  transition: background-color 0.3s;
  z-index: 4;
  border-radius: 50%;
  position: absolute;
}

.move-btn:hover {
  background-color: rgba(0, 0, 0, 0.8);
}

.left-btn {
  left: 15%;
}

.right-btn {
  right: 15%;
}

.photo-stack {
  position: relative;
  width: 100%;
  max-width: 1200px;
  height: 500px;
  margin: 0 auto;
  perspective: 1000px;
}

.photo {
  position: absolute;
  width: 50%;
  height: 80%;
  left: 25%;
  top: 25%;
  transform-style: preserve-3d;
}

.photo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 12px;
}

@media (max-width: 768px) {
  .photo {
    width: 70%;
  }
  
  .move-btn {
    padding: 10px 20px;
    font-size: 24px;
  }
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
