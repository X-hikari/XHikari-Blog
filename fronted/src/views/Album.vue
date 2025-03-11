<template>
  <div class="album-main-content">
    <!-- 相册页面标题 -->
    <h1 class="album-title">Xhikariの相册</h1>
    
    <!-- 相册卡片容器 -->
    <div class="album-grid">
      <AlbumCard v-for="album in albums"
        :id="album.id"
        :name="album.name"
        :imageSrc="album.imageSrc"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import AlbumCard from '@/components/Album/AlbumCard.vue';

const albums = ref([]);

const fetchAlbums = async () => {
  try {
    const response = await fetch('http://localhost:8001/api/albums/');
    const data = await response.json();

    albums.value = data.map(album => ({
      id: album.id,
      name: album.name,
      // 直接使用 `imageSrc`，如果为空，则提供一个默认封面
      imageSrc: album.imageSrc ? album.imageSrc : ['']
    }));
  } catch (error) {
    console.error('获取相册数据失败:', error);
  }
};

onMounted(() => {
  fetchAlbums();
});
</script>

<style scoped>
.album-main-content {
  width: 75%;
  margin: 160px auto;
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
