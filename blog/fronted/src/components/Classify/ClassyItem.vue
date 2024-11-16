<template>
  <ul>
    <li v-for="(category, index) in categories" :key="category.id" ref="categoryItems">
      <div>
        <span class="classifyname">{{ category.name }}</span>
        <span class="articlecount" v-if="category.children && category.children.length === 0">  — —  ({{ category.article_count }})</span>
      </div>

      <!-- 如果当前分类有子分类，则递归渲染子分类 -->
      <!-- <ClassifyItem v-if="category.children && category.children.length > 0" :categories="category.children" /> -->
      <ClassifyItem 
        v-if="category.children && category.children.length > 0" 
        :categories="category.children"
        :ref="el => { if (el) childComponents[category.id] = el; }"
      />
    </li>
  </ul>
</template>
  
<script setup>
import { ref, nextTick } from 'vue';
import ClassifyItem from '@/components/Classify/ClassyItem.vue';

const props = defineProps({
  categories: {
    type: Array,
    required: true
  },
  activeRoot: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['update-active-root']);
// 记录所有 `li` 元素的引用
const categoryItems = ref([]);
const childComponents = ref({});
const buffer = 50; // 触发位置距离顶部的缓冲距离

const checkCategories = () => {
  let result = -1;
  let temp = -1;
  // console.log("categories:", props.categories);
  // console.log("categoryItems", categoryItems.value);
  // 遍历当前目录
  props.categories.forEach((category, index) => {
    const el = categoryItems.value[index]; // 获取对应的 DOM 元素
    if (el) {
      const rect = el.getBoundingClientRect();
      // 如果该目录项在视口内
      if (rect.top <= buffer) {
        // emit('update-active-root', category.id);
        result = category.id;
        console.log("result", result);

        // 如果目录有子目录，处理子目录
        if (category.children && category.children.length > 0) {
          const specificChild = childComponents.value[category.id];
          console.log("进入子目录", specificChild);
          if (specificChild) {
            console.log("temp1", temp);
            temp = specificChild.checkCategories(); // 确保子组件方法可用
            console.log("temp2", temp);
            if (temp && temp !== -1) {
              result = temp;
            }
          }
        }
        console.log("每次返回的result", result);
      }
    }
  });
  return result;
};

// 使用 defineExpose 暴露方法
defineExpose({
  checkCategories
});
</script>
  
<style scoped>
ul {
  list-style-type: none;
  padding-left: 10px;
  margin-left: 20px;
}
  
.classifyname {
    /* background-color: rgba(255, 255, 255, 0.8); */
    border-radius: 5px;
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
  