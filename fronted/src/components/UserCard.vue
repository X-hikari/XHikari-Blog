<template>
  <div class="user-card">
    <!-- 背景图片区域 -->
    <div class="user-card__cover">
      <img src="/UserCard/background.jpg" alt="Cover Image" class="cover-image" />
      <div class="overlay">
        <img src="/UserCard/avatar_xhikari.png" alt="Avatar" class="avatar" />
        <h3 class="username">小肖的个人博客</h3>
        <p class="status">学不动了、学不懂了、学不会了</p>
      </div>
    </div>

    <!-- 统计数据 -->
    <div class="user-card__stats">
      <div>
        <span>文章 </span>
        <span> {{ articleNumber }}</span>
      </div>
      <div>
        <span>分类 </span>
        <span> {{ categoryNumber }}</span>
      </div>
      <div>
        <span>相册 </span>
        <span> {{ albumNumber }}</span>
      </div>
    </div>

    <!-- 社交图标 -->
    <div class="user-card__social-icons">
      <!-- 微信 -->
    <div class="icon-container" @mouseenter="hoveredIcon = '微信'" @mouseleave="hoveredIcon = null">
      <i class="iconfont icon-weixin" @click.stop></i>
      <div v-show="hoveredIcon === '微信'" class="qrcode-container">
        <img src="/relation/Wechat-QRcode.jpg" alt="微信二维码" class="qrcode">
      </div>
    </div>

    <!-- QQ -->
    <div class="icon-container" @mouseenter="hoveredIcon = 'QQ'" @mouseleave="hoveredIcon = null">
      <i class="iconfont icon-QQ" @click.stop></i>
      <div v-show="hoveredIcon === 'QQ'" class="qrcode-container">
        <img src="/relation/QQ-QRcode.jpg" alt="QQ二维码" class="qrcode">
      </div>
    </div>
      <i class="iconfont icon-github-fill" @click="openLink('https://github.com/X-hikari/XHikari-Blog')"></i>
      <i class="iconfont icon-bilibili-line" @click="openLink('https://space.bilibili.com/505788992?spm_id_from=333.1007.0.0')"></i>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const hoveredIcon = ref(null)

const props = defineProps({
  articleNumber: {
    type: Number,
    default: 0
  },
  categoryNumber: {
    type: Number,
    default: 0
  },
  albumNumber: {
    type: Number,
    default: 0
  }
})

const openLink = (link) => {
  if (typeof window !== 'undefined') {
    window.open(link, '_blank');
  }
}
</script>

<style scoped>
.user-card {
  width: 100%;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  /* overflow: hidden; */
  text-align: center;
  font-family: Arial, sans-serif;
  user-select: none;
  outline: none !important;
}

.user-card__cover {
  position: relative;
}

.cover-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  opacity: 0.8;
}

.overlay {
  position: absolute;
  top: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 3px solid white;
}

.username {
  font-size: 1.2em;
  font-weight: bold;
  margin: 10px 0 5px;
}

.status {
  color: #f0f0f0;
  font-size: 0.9em;
}

.user-card__stats {
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}

.user-card__stats div {
  text-align: center;
}

.user-card__stats span:first-child {
  color: #8b5c5c;
}

.user-card__stats span:last-child {
  font-weight: bold;
}

.user-card__social-icons {
  display: flex;
  justify-content: center;
  gap: 10px;
  padding: 10px 0;
}

.user-card__social-icons i {
  font-size: 1.5em;
  cursor: pointer;
}

.user-card__social-icons i:hover {
  color: #0073e6;
}

.icon-container {
  position: relative;
  cursor: pointer;
  transition: transform 0.2s;
}

.icon-container:hover {
  transform: scale(1.1);
}

.qrcode-container {
  position: absolute;
  top: 120%;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  z-index: 1000;
}

.qrcode {
  width: 200px;
  height: 260px;
  display: block;
}

/* 二维码箭头样式 */
.qrcode-container::after {
  content: "";
  position: absolute;
  top: -16px;
  left: 50%;
  transform: translateX(-50%);
  border-width: 8px;
  border-style: solid;
  border-color: transparent transparent white transparent
}
</style>
