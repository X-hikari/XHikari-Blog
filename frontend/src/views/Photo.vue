<template>
  <div class="main-photos-content">
    <h2 class="album-title">{{ albumName }}</h2>

    <!-- 模式选择 -->
    <div class="model">
      <div class="icon-btn left-icon" title="大图模式" @click="toggleMode('big')">
        <i class="iconfont icon-datumoshi" style="font-size: 30px;"></i>
        <span class="icon-tooltip">大图模式</span>
      </div>
      <div class="icon-btn right-icon" title="列表模式" @click="toggleMode('list')">
        <i class="iconfont icon-list" style="font-size: 30px;"></i>
        <span class="icon-tooltip">列表模式</span>
      </div>
    </div>

    <!-- 动态加载子组件 -->
    <component :is="currentMode" :images="images" :albumName="albumName" />
  </div>
</template>

<script setup>
import { ref, onMounted, markRaw } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import PhotoBig from '@/components/Album/PhotoBig.vue';
import PhotoList from '@/components/Album/PhotoList.vue';

const route = useRoute();
const albumId = ref(route.query.albumId);
const albumName = ref('');
const images = ref([]);
const currentMode = ref(markRaw(PhotoBig)); // 默认加载大图模式

onMounted(() => {
  axios
    .get(`http://localhost:8001/api/albumPhotos?albumId=${albumId.value}`)
    .then((response) => {
      images.value = response.data.photos;
      albumName.value = response.data.albumName;
    })
    .catch((error) => {
      console.error('Error fetching album photos:', error);
    });
});

const toggleMode = (mode) => {
  // 根据选择的模式切换组件
  currentMode.value = mode === 'big' ? markRaw(PhotoBig) : markRaw(PhotoList);
};
</script>

<style scoped>
.main-photos-content {
  text-align: center;
  margin: 160px auto;
  padding-bottom: 160px;
  user-select: none;
}

.album-title {
  font-size: 4rem;
  margin-bottom: 40px;
}

.model {
  position: fixed;
  top: 80px;
  right: 20px;
  display: flex;
  gap: 10px;
}

.icon-btn {
  font-size: 30px;
  cursor: pointer;
  position: relative;
  z-index: 10;
}

.icon-tooltip {
  display: none;
  position: absolute;
  top: -30px;
  font-size: 12px;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 5px;
  border-radius: 4px;
  white-space: nowrap;
}

.icon-btn:hover .icon-tooltip {
  display: block;
}
</style>
