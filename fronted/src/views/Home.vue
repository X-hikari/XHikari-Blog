<template>
  <!-- 顶部图片 -->
  <div class="background-image">
    <img :src="imageSrc" alt="Background Image" />
    <div class="theme">{{ themeText }}</div>
    <div class="overlay-text">{{ displayedText }}</div>
    <div class="icon-circle" @click="scrollToContentBottom">
      <i class="iconfont icon-arrow-down-s-line" style="font-size: 30px;"></i>
    </div>
    <Wave />
  </div>

  <!-- 下方的内容部分 -->
  <div class="content-bottom">
    <div class="left-part">
      <Announcement />
      <WebSite />
      <div class="sticky-header">
        <UserCard
          :articleNumber="articleNumber"
          :categoryNumber="categoryNumber"
          :albumNumber="albumNumber"
        /> <!-- 左侧部分：UserCard 卡片 -->
      </div>
    </div>
    <div class="right-part">
      <!-- 右侧部分：文章卡片 -->
      <ArticleCard
        v-for="(article, index) in paginatedArticles"
        :key="index"
        :id="article.id"
        :title="article.title"
        :summary="article.summary"
        :date="article.updated_at"
        :views="article.visits"
        :imageSrc="article.imageSrc"
      />
      <!-- 分页控件 -->
      <Pagination 
        :page="page" 
        :totalPages="totalPages" 
        @changePage="changePage" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import axios from 'axios';  // 确保导入 axios
import Wave from '@/components/Wave.vue'
import UserCard from '@/components/UserCard.vue'
import ArticleCard from '@/components/ArticleCard.vue'
import Announcement from '@/components/Announcement.vue'
import WebSite from '@/components/WebSite.vue'
import Pagination from '@/components/Pagination.vue'; // 引入分页组件

const imageSrc = ref('/homeBackground.jpg');
const themeText = "Xhikari's Blog";
const fullText = '与你在此的相遇\n就是命运石之门的选择';
const displayedText = ref('');
const articles = ref([]);  // 声明 articles
const page = ref(1);  // 当前页数
const pageSize = 8;  // 每页显示 8 个文章

const articleNumber = ref(0);
const categoryNumber = ref(0);
const albumNumber = ref(0);

// 控制文字显示的定时器
let interval = null;

onMounted(() => {
  let index = 0;
  interval = setInterval(() => {
    if (index < fullText.length) {
      displayedText.value += fullText[index];
      index++;
    } else {
      clearInterval(interval);
    }
  }, 200);

  // 获取文章数据
  axios.get('http://localhost:8001/api/articles/')
    .then(response => {
      articles.value = response.data;
    })
    .catch(error => {
      console.error('Error fetching articles:', error);
    });

  axios.get('http://localhost:8001/api/homenumber/')
  .then(response => {
    articleNumber.value = response.data.article_count;
    categoryNumber.value = response.data.category_count;
    albumNumber.value = response.data.album_count;
    // console.log(articleNumber.value);
  })
  .catch(error => {
    console.error('Error fetching articles:', error);
  });
});

onUnmounted(() => {
  clearInterval(interval);
});

const scrollToContentBottom = () => {
  const contentBottom = document.querySelector('.content-bottom');
  if (contentBottom) {
    contentBottom.scrollIntoView({
      behavior: 'smooth',  // 平滑滚动
      block: 'start',      // 滚动到目标元素的顶部
    });
  }
}

// 计算分页后的文章
const totalPages = computed(() => {
  return Math.ceil(articles.value.length / pageSize);
});

const paginatedArticles = computed(() => {
  const startIndex = (page.value - 1) * pageSize;
  return articles.value.slice(startIndex, startIndex + pageSize);
});

// 改变当前页
const changePage = (newPage) => {
  if (newPage >= 1 && newPage <= totalPages.value) {
    page.value = newPage;
  }
};
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
  background-color: rgba(0, 0, 0, 0.5);
  padding: 0.5em 1em;
  border-radius: 8px;
  white-space: pre-wrap;
}

.icon-circle {
  position: absolute;
  bottom: 15%;
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
  cursor: pointer;
}

.content-bottom {
  display: flex;
  width: 100%;
  margin-top: 0px;
  background-color: rgba(241, 249, 254, 1);
  z-index: 2;
  /* align-items: flex-start; */
  align-items: stretch;
}

.left-part {
  width: 30%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 15px;
  padding-left: 180px;
}

.left-part > * {
  margin-bottom: 15px; /* 设置子元素之间的间隔 */
}

.sticky-header {
  position: -webkit-sticky; /* Safari 支持的前缀 */
  position: sticky;
  top: 50px; /* 设置距离页面顶部的固定距离 */
  padding: 10px;
}

.right-part {
  width: 60%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 15px;
  gap: 20px;
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
