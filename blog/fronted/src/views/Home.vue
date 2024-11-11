<template>
  
  <!-- 顶部图片 -->
  <div class="background-image">
    <img :src="imageSrc" alt="Background Image" />
    <div class="theme">{{ themeText }}</div>
    <!-- 随时间出现的文字 -->
    <div class="overlay-text">{{ displayedText }}</div>
    <div class="icon-circle">
      <i class="iconfont icon-arrow-down-s-line" style="font-size: 30px;"></i>
    </div>
  </div>

</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { gsap } from 'gsap';

const name = 'Home';
const imageSrc = ref('/homeBackground.jpg');
const themeText = "Xhikari's Blog"
const fullText = '你我在此相遇\n就是命运石之门的选择'; // 使用 \n 换行
const displayedText = ref(''); // 当前显示的文本

// 控制文字显示的定时器
let interval = null;

onMounted(() => {
  let index = 0; // 当前显示的字符索引
  interval = setInterval(() => {
    if (index < fullText.length) {
      displayedText.value += fullText[index]; // 每次添加一个字符
      index++;
    } else {
      clearInterval(interval); // 完整显示后清除定时器
    }
  }, 200);
});

onUnmounted(() => {
  clearInterval(interval);
});

</script>

<style scoped>
.background-image {
  width: 100%;
  overflow: hidden;
  position: relative;
}

.background-image img {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
  object-position: left;
  opacity: 0;
  animation: imageAnimation 30s linear 1 forwards;
  backface-visibility: hidden;
  transform-style: preserve-3d;
}

.background-image .theme {
  position: absolute;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #C0C0C0;
  font-size: 6em;
  font-weight: bold;
  text-align: center;
  /* background-color: rgba(0, 0, 0, 0.5); */
  padding: 0.5em 1em;
  border-radius: 8px;
}

.overlay-text {
  position: absolute;
  top: 60%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 2em;
  text-align: center;
  background-color: rgba(0, 0, 0, 0.5); /* 背景遮罩以提升文字可读性 */
  padding: 0.5em 1em;
  border-radius: 8px;
  white-space: pre-wrap; /* 保持换行效果 */
}

/* 圆形图标样式 */
.icon-circle {
  position: absolute;
  bottom: 10%; /* 距离底部 */
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 40px;
  background-color: rgba(0, 0, 0, 0.6);
  color: #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

@keyframes imageAnimation {
  0% {
    opacity: 0;
    animation-timing-function: ease-in;
  }

  2% {
    opacity: 0.2;
  }

  8% {
    opacity: 0.8;
    transform: scale(1.05);
    animation-timing-function: ease-out;
  }

  17% {
    opacity: 1;
    transform: scale(1.1);
  }

  25% {
    opacity: 1;
    transform: scale(1.1);
  }

  100% {
    opacity: 1;
  }
}

</style>
