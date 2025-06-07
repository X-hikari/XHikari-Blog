<template>
  <div class="container">
    <div class="header">我的空间</div>
    <div class="content">
      <div class="left-panel">
        <!-- 左侧内容，暂时留空 -->
         <EmotionCalendar
         class="sticky-header"
         :date-list="dateList"
         @updateDate="updateDate"
         />
      </div>
      <div class="right-panel">
        <div ref="loadTrigger" class="load-trigger"></div>
        <EmotionCard v-for="(emotion, index) in visibleEmotions" 
          :key="index" 
          :text="emotion.content" 
          :images="emotion.images" 
          :created_at="emotion.created_at" 
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import axios from 'axios';
import EmotionCard from "@/components/Emotion/EmotionCard.vue";
import EmotionCalendar from "@/components/Emotion/EmotionCalendar.vue";

const emotions = ref([]);
const visibleEmotions = ref([]);
const loadTrigger = ref(null);
const batchSize = 5; // 每次加载的数量
let loadedCount = 0;

const dateList = ref([]);
const date = ref("");

const loadMore = () => {
  if (loadedCount < emotions.value.length) {
    visibleEmotions.value.push(...emotions.value.slice(loadedCount, loadedCount + batchSize));
    loadedCount += batchSize;
  }
};

const onScroll = () => {
  if (loadTrigger.value) {
    const rect = loadTrigger.value.getBoundingClientRect();
    if (rect.top < window.innerHeight) {
      loadMore();
    }
  }
};

onMounted(() => {
  axios.get(`http://localhost:8001/api/emotions/`)
  .then(response => {
    emotions.value = response.data.data;
    dateList.value = emotions.value.map(item => item.created_at);
    loadMore(); // 初次加载
    window.addEventListener('scroll', onScroll);
  });

});

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll);
});

const fetchEmotions = async () => {
  const params = ref({});
  if (date) {
    params.date = date.value;
  }
  const response = await axios.get("http://localhost:8001/api/emotions/", {
    params,
  });
  if (response.status == 200) {
    emotions.value = response.data.data;
    visibleEmotions.value = [];
    loadedCount = 0;
    loadMore(); // 初次加载
    window.addEventListener('scroll', onScroll);
  }
}

const updateDate = async (querydate) => {
  date.value = querydate;
  fetchEmotions();
}
</script>

<style scoped>
.container {
  width: 65%;
  margin: 100px auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.header {
  width: 100%;
  text-align: center;
  font-size: 2em;
  font-weight: bold;
  padding: 16px;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  margin-bottom: 20px;
}

.content {
  display: flex;
  width: 90%;
  max-width: 1200px;
  gap: 5%;
}

.left-panel {
  width: 30%;
  border-radius: 12px;
  padding: 16px;
  min-height: 400px;
}

.right-panel {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.load-trigger {
  width: 100%;
  height: 10px;
}

.sticky-header {
  position: -webkit-sticky; /* Safari 支持的前缀 */
  position: sticky;
  top: 50px; /* 设置距离页面顶部的固定距离 */
  padding: 10px;
}
</style>