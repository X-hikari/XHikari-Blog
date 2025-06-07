<template>
  <canvas ref="canvas" @click="handleClick"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";

const props = defineProps({
  messages: Array,
});
const emit = defineEmits(["click-star"]);

const canvas = ref(null);
let ctx = null;
let stars = [];
const STAR_SPEED = 0.1; // 速度降低，让流星更缓慢
const STAR_COUNT = 10; // 控制最大流星数量

// 初始化 Canvas
onMounted(() => {
  canvas.value.width = window.innerWidth;
  canvas.value.height = window.innerHeight;
  ctx = canvas.value.getContext("2d");
  window.addEventListener("resize", resizeCanvas);

//   console.log(props.messages);
  // 如果 messages 为空，不生成流星
  if (props.messages.length > 0) {
    generateStars(); // 生成初始流星
    animate(); // 启动动画
  }
});

onUnmounted(() => {
  window.removeEventListener("resize", resizeCanvas);
});

// 监听窗口变化
const resizeCanvas = () => {
  canvas.value.width = window.innerWidth;
  canvas.value.height = window.innerHeight;
};

// 生成初始流星
const generateStars = () => {
  stars = [];
  // 确保每个流星对应一条留言，并且当留言过多时，循环显示
  const messageCount = props.messages.length;
  for (let i = 0; i < STAR_COUNT; i++) {
    // 使用留言的索引来循环生成流星
    addStar(props.messages[i % messageCount]); // 绑定留言
  }
};

// 添加流星
const addStar = (message = null) => {
  const x = Math.random() * canvas.value.width;
  const y = Math.random() * canvas.value.height * 0.5;
  const speed = Math.random() * 2 + STAR_SPEED;
  const length = Math.random() * 30 + 20; // 控制流星的尾巴长度
  const opacity = Math.random() * 0.5 + 0.5; // 控制透明度

  stars.push({ x, y, speed, length, opacity, message });
};

// 动画循环
const animate = () => {
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height);

  stars.forEach((star) => {
    star.x -= star.speed;
    star.y += star.speed * 0.5;
    drawStar(star);

    // 当流星飞出屏幕时，重新放回顶部
    if (star.x < -10 || star.y > canvas.value.height) {
      star.x = Math.random() * canvas.value.width;
      star.y = Math.random() * canvas.value.height * 0.5;
      star.speed = Math.random() * 2 + STAR_SPEED;
    }
  });

  requestAnimationFrame(animate);
};

// 绘制流星（带尾巴 + 透明度）
const drawStar = (star) => {
  const gradient = ctx.createLinearGradient(star.x, star.y, star.x + star.length, star.y - star.length);
  gradient.addColorStop(0, `rgba(255,255,255,${star.opacity})`);
  gradient.addColorStop(1, "rgba(255,255,255,0)");

  ctx.strokeStyle = gradient;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(star.x, star.y);
  ctx.lineTo(star.x + star.length, star.y - star.length);
  ctx.stroke();
};

// 点击流星
const handleClick = (event) => {
  const { offsetX, offsetY } = event;
  for (const star of stars) {
    // 判断点击范围，点击流星后触发事件
    if (Math.hypot(star.x - offsetX, star.y - offsetY) < 15) {
      emit("click-star", star.message);
      break;
    }
  }
};

// 监听消息变动，动态添加流星
watch(
  () => props.messages,
  (newMessages) => {
    if (newMessages.length > 0) {
      // 如果 messages 数组有内容，且流星少于最大数量，添加流星
      stars = []; // 清空当前的流星
      generateStars(); // 重新生成流星
    } else {
      // 如果 messages 数组为空，清空流星
      stars = [];
    }
  },
  { deep: true }
);
</script>

<style scoped>
canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
