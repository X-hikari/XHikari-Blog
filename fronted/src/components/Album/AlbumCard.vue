<template>
  <div class="album-container" @mouseenter="isHovered = true" @mouseleave="isHovered = false">
    <!-- 左侧开口盒子效果，盖住部分图片 -->
    <div class="box-left">
      <span class="album-name">相册名字</span>
    </div>
    <div 
      v-for="(img, index) in images" 
      :key="index"
      class="photo-stack"
      :style="{
        zIndex: images.length - index,
        transform: getTransform(index),
        transition: `transform ${0.3 + index * 0.1}s ease-out`
      }"
    >
      <img 
        :src="img" 
        class="photo" 
        alt="photo"
        @load="handleImageLoad($event, index)"
        :style="{ objectFit: objectFitStyles[index] || 'cover' }"
      >
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

const images = [
  '/UserCard/background.jpg',
];

const isHovered = ref(false);
// 用于存储每张图片对应的 object-fit 样式
const objectFitStyles = reactive({});

// 与 CSS 中容器尺寸一致
const containerWidth = 150;
const containerHeight = 200;
const containerRatio = containerWidth / containerHeight;

function handleImageLoad(event, index) {
  const naturalWidth = event.target.naturalWidth;
  const naturalHeight = event.target.naturalHeight;
  const imageRatio = naturalWidth / naturalHeight;
  if (Math.abs(imageRatio - containerRatio) / containerRatio < 0.1) {
    objectFitStyles[index] = 'contain';
  } else {
    objectFitStyles[index] = 'cover';
  }
}

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
  /* object-fit 根据图片比例在加载后动态设置 */
  transition: transform 0.3s;
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
  font-size: 14px;
  color: #333;
}
</style>
