<template>
  <ul>
    <li v-for="category in categories" :key="category.id">
      <div>
        <span>{{ category.name }}</span>
        <span class="articlecount" v-if="category.children && category.children.length === 0">  — —  ({{ category.article_count }})</span>
      </div>

      <!-- 如果当前分类有子分类，则递归渲染子分类 -->
      <ClassifyItem v-if="category.children && category.children.length > 0" :categories="category.children" />
    </li>
  </ul>
</template>
  
<script setup>
import ClassifyItem from '@/components/Classify/ClassyItem.vue';
// 接收父组件传入的分类数据
const props = defineProps({
  categories: {
    type: Array,
    required: true
  }
});
</script>
  
<style scoped>
ul {
  list-style-type: none;
  margin-left: 20px; /* 为子分类加上缩进 */
}
  
li {
  margin-bottom: 10px;
}
  
span {
  font-weight: bold;
}
  
.articlecount {
  margin-left: 5%;
}
</style>
  