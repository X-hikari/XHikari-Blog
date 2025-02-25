<template>
  <div class="album-main-content">
    <!-- 相册页面标题 -->
    <h1 class="album-title">我的相册</h1>
    
    <!-- 相册卡片容器 -->
    <div class="album-grid">
      <AlbumCard v-for="index in 6" :key="index" />
    </div>
  </div>
</template>

<script setup>
import AlbumCard from '@/components/Album/AlbumCard.vue';
</script>

<style scoped>
.album-main-content {
  width: 75%;
  margin: 0 auto;
  text-align: center;
}

.album-title {
  font-size: 4em;
  font-weight: bold;
  margin-bottom: 20px;
  color: rgba(0, 255, 255, 0.906);
}

.album-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  justify-content: center;
}
</style>
