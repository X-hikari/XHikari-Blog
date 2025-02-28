<template>
  <div class="content">
    <div class="introduction" v-if="data">
      <!-- 文章标题 -->
      <div class="categoryDetailTitle">{{ data.name }}</div>

      <!-- 元信息 -->
      <div class="category-meta">      
        <!-- 时间信息 -->
        <div class="meta-row">
          <span class="meta-item">创建时间：{{ data.created_at }}</span>
          <span class="meta-item">更新时间：{{ data.updated_at }}</span>
        </div>
      </div>
      
      <!-- Banner 图（如果有） -->
      <div v-if="data.banner_url" class="category-bannar">
        <img :src="`http://localhost:8001${data.banner_url}`" alt="Banner" />
      </div>
  
      <!-- 摘要（如果有） -->
      <div v-if="data.description" class="category-summary">
        {{ data.description }}
      </div>
    </div>
    <div class="cards">
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
const name ="Catgory"
import { ref, onMounted, computed } from 'vue'
import axios from 'axios';  // 确保导入 axios
import { useRoute } from 'vue-router'; // 用于获取路由参数
import Pagination from '@/components/Pagination.vue'; // 引入分页组件
import ArticleCard from '@/components/ArticleCard.vue';

const route = useRoute();
const categoryId = ref(route.query.categoryId); // 获取 URL 中的 id 参数
const articles = ref([]);  // 声明 articles
const page = ref(1);  // 当前页数
const pageSize = 8;  // 每页显示 8 个文章
const data = ref(null);

onMounted(() => {
  axios.get(`http://localhost:8001/api/category?id=${categoryId.value}`)
  .then(response => {
    data.value = response.data;
    console.log(data.value.banner_url);
  })
  .catch(error => {
    console.error('Error fetching articles:', error);
  });
  // 获取文章数据
  axios.get(`http://localhost:8001/api/articles?id=${categoryId.value}`)
  .then(response => {
    articles.value = response.data;
    // console.log(articles.value);
  })
  .catch(error => {
    console.error('Error fetching articles:', error);
  });
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

.introduction {
  width: 60%;
  background-color: rgba(251, 248, 247, 0.8);
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  padding: 20px;
  backdrop-filter: blur(5px);
}

.category-bannar img {
  width: 100%;
  height: auto;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 10px;
}

.categoryDetailTitle {
  font-size: 2.5em;
  padding-top: 3%;
  text-align: center;
  color: #333;
  font-weight: bold;
  margin: 0 auto;
  max-width: 80%;
  line-height: 1.2;
  padding-bottom: 2%;
}

.category-summary {
  font-size: 1em;
  margin: 20px 0;
  color: #555;
  line-height: 1.5;
}

.category-meta {
  font-size: 0.9em;
  color: #555;
  margin-bottom: 15px;
}

.meta-row {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 5px;
}

.meta-item {
  margin-right: 10px;
}

.meta-item strong {
  color: #333;
}

.cards {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 15px;
  justify-content: center;
}
</style>