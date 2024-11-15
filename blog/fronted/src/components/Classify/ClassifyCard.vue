<template>
  <div class="classifycard">
    <div class="title">文章总览</div>
    <div class="introduce">文章分类如下，点击可以跳转</div>
    <div class="section">
      <ul>
        <li v-for="category in categories" :key="category.id">
          <div>
            <span class="parentclassify">{{ category.name }}</span>
            <div class="articlenumber">共 {{ category.article_count }} 篇</div>
          </div>

          <!-- 递归渲染子分类 -->
          <ClassifyItem v-if="category.children && category.children.length > 0" :categories="category.children" />
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ClassifyItem from '@/components/Classify/ClassyItem.vue';

// 接收父组件传入的 props
const props = defineProps({
  categories: {
      type: Array,
      required: true
    }
});

</script>

<style scoped>
.classifycard {
  width: 100%;
  background-color: rgba(251, 248, 247, 0.4);
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  padding: 20px;
  backdrop-filter: blur(1px);
}

.title {
  font-size: 1.5em;
  color: rgba(123, 162, 255);
  font-weight: bold;
  text-align: center;
  margin-bottom: 1em;
}

.introduce {
  padding: 1em;
  background-color: #7889e8;
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  font-size: 0.8em;
  text-align: center;
  color: white;
  font-weight: bold;
  margin-bottom: 1em;
}

.section {
  width: 100%;
  height: auto;
}

.classifyheader {
  width: 100%;
  color: #91c4ee;
}

ul {
  padding-left: 1%;
  list-style-type: none;
  gap: 5%;
}

li {
  margin-bottom: 8%;
  align-items: center;
  font-weight: bold;
}

.parentclassify {
  align-items: center;
  font-weight: bold;
  font-size: 1.2em;
  position: relative;
  padding-left: 10px;
}

.parentclassify::before {
  top: 10%;
  content: '';
  position: absolute;
  left: 0;
  width: 5px;
  height: 100%;
  background-color: rgba(145, 196, 238);
  border-radius: 3px;
}

.articlenumber {
  display: block; /* 让该元素独占一整行 */
  font-size: 0.7em; /* 设置较小的文字 */
  font-weight: bold;
  color: white; /* 设置文字颜色为白色 */
  background-color: #4fa3f7; /* 蓝色背景 */
  padding: 2.5px 15px; /* 给框加一些内边距 */
  border-radius: 6px; /* 圆角效果 */
  text-align: center;
  margin-top: 10px;
  margin-bottom: 5px;
  width: fit-content;
}
</style>
