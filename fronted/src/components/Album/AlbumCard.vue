<template>
  <div class="album-container" @mouseenter="isHovered = true" @mouseleave="isHovered = false" @click="goToAlbum(id)">
    <!-- 左侧开口盒子效果，盖住部分图片 -->
    <div class="box-left">
      <span class="album-name">{{ name }}</span>
    </div>
    
    <div 
      v-for="(img, index) in imageSrc" 
      :key="index"
      class="photo-stack"
      :style="{
        zIndex: imageSrc.length - index,
        transform: getTransform(index),
        transition: `transform ${0.3 + index * 0.1}s ease-out`
      }"
    >
      <template v-if="img">
        <img 
          :src="`http://localhost:8001${img}`" 
          class="photo" 
          alt="photo"
          :style="{ objectFit: objectFitStyles[index] || 'cover' }"
        >
      </template>
      <template v-else>
        <div class="placeholder">该相册暂无图片</div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps({
  id: {
    type: Number,
    required: true
  },
  name: {
    type: String,
    required: true
  },
  imageSrc: {
    type: Array,
    default: ['']  // 允许空列表作为默认值
  }
});

const isHovered = ref(false);
// 用于存储每张图片对应的 object-fit 样式
const objectFitStyles = reactive({});

const goToAlbum = (albumId) => {
  // 使用 Vue Router 的编程式导航
  router.push({ path: '/photo', query: { albumId } });
};

const getTransform = (index) => {
  if (index === 0) {
    return isHovered.value 
      ? 'rotateY(-25deg) translateX(20px)'
      : 'rotateY(0deg)';
  }
  return `rotateY(${2 * (index + 1)}deg) translateZ(-${index * 10}px)`;
};
</script>

<style scoped>
.album-container {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 25px auto;
  perspective: 1200px;
  /* 允许显示超出容器的部分，保证左侧盒子能显示 */
  overflow: visible;
  cursor: pointer;
}

.photo-stack {
  position: absolute;
  width: 100%;
  height: 100%;
  transform-origin: left center;
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
  border-radius: 5px;
  overflow: hidden;
  backface-visibility: hidden;
}

.photo {
  width: 100%;
  height: 100%;
  transition: transform 0.3s;
}

.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background-color: #f0f0f0;
  color: #666;
  font-size: 14px;
  text-align: center;
  border-radius: 5px;
}

/* 左侧开口盒子效果：略高于图片，并垂直居中，同时禁止光标与文本选择 */
.box-left {
  position: absolute;
  top: 50%;
  left: -10px;
  width: 40px;
  height: 110%;
  background: #f2ca00;
  border: 1px solid #ccc;
  border-right: none;
  border-radius: 5px 0 0 5px;
  transform: translateY(-50%) perspective(1200px) rotateY(0);
  box-shadow: -5px 0 15px rgba(0,0,0,0.2);
  z-index: 100;
  cursor: default;
  user-select: none;
  pointer-events: none;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 竖排显示的相册名字 */
.album-name {
  writing-mode: vertical-rl;
  text-orientation: upright;
  font-size: bold;
  color: #333;
}
</style>
