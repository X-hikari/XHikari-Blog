<template>
  <div>
    <div v-if="q" class="search-title">
      <div class="search-title-text">搜索结果</div>
    </div>

    <div v-if="loading">加载中...</div>
    <div v-else class="content">
      <div v-if="articles.length === 0" class="no-results">
        <p>没有搜索结果，请更换关键词重新搜索。</p>
      </div>

      <div v-else class="cards">
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
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute } from 'vue-router'; // 用于获取路由参数
import axios from 'axios';  // 确保导入 axios
import Pagination from '@/components/Pagination.vue'; // 引入分页组件
import ArticleCard from '@/components/ArticleCard.vue';

const route = useRoute();
const q = ref(route.query.q || ''); // 获取查询参数，默认为空字符串
const articles = ref([]);  // 声明 articles
const page = ref(1);  // 当前页数
const pageSize = 8;  // 每页显示 8 个文章

const fetchArticles = () => {
  const params = q.value ? { q: q.value } : {};
  axios.get('http://localhost:8001/api/searcharticles/', { params })
    .then(response => {
      articles.value = response.data.results || [];
    })
    .catch(error => {
      console.error('获取文章失败:', error);
    });
};

// 监听路由变化，特别是查询参数的变化
watch(() => route.query.q, (newQuery) => {
  q.value = newQuery || '';
  fetchArticles(); // 重新获取文章数据
}, { immediate: true });

onMounted(() => {
  fetchArticles();
});

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
.content {
  width: 100%;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
  flex-direction: column;
}

.search-title {
  width: 60%;
  margin: 0 auto;
  padding: 15px 0;
  margin-bottom: 20px;
  text-align: center;
  background-color: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 8px;
}

.search-title-text {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.no-results {
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  color: #888;
  text-align: center;
}

.cards {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 15px;
  justify-content: center;
}
</style>
