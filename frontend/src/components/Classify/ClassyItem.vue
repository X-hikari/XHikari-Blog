<template>
  <ul>
    <li v-for="(category, index) in categories" :key="category.id" ref="categoryItems">
      <div>
        <span class="classifyname" 
        @click="category.children && category.children.length === 0 ? goToCategory(category.id) : null" 
        :class="{ 'clickable': category.children && category.children.length === 0 }">
        {{ category.name }}</span>
        <span class="articlecount" v-if="category.children && category.children.length === 0">  — —  ({{ category.article_count }})</span>
      </div>

      <!-- 如果当前分类有子分类，则递归渲染子分类 -->
      <!-- <ClassifyItem v-if="category.children && category.children.length > 0" :categories="category.children" /> -->
      <ClassifyItem 
        v-if="category.children && category.children.length > 0" 
        :categories="category.children"
        :jumpRoot="jumpRoot"
        :ref="el => { if (el) childComponents[category.id] = el; }"
      />
    </li>
  </ul>
</template>
  
<script setup>
import { ref, nextTick, watch } from 'vue';
import ClassifyItem from '@/components/Classify/ClassyItem.vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  categories: {
    type: Array,
    required: true
  },
  jumpRoot: {
    type: Number,
    required: true
  },
});

const emit = defineEmits(['update-active-root']);
// 记录所有 `li` 元素的引用
const categoryItems = ref([]);
const childComponents = ref({});
const buffer = 50; // 触发位置距离顶部的缓冲距离
const router = useRouter();

const goToCategory = (categoryId) => {
  // 使用 Vue Router 的编程式导航
  router.push({ path: '/category', query: { categoryId } });
}

const scrollToCategory = (categoryId) => {
  nextTick(() => {
    const targetIndex = props.categories.findIndex((category) => category.id === categoryId);
    if (targetIndex !== -1 && categoryItems.value[targetIndex]) {
      const targetElement = categoryItems.value[targetIndex];
      const rect = targetElement.getBoundingClientRect();
      // 获取目标元素的顶部距离文档的偏移量
      const offsetTop = rect.top + window.scrollY;

      // 滚动到目标位置，距离顶部50px
      window.scrollTo({
        top: offsetTop - buffer+5, // 调整50px
        behavior: 'smooth',  // 平滑滚动
      });
    }
  });
};

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
        // console.log("result", result);

        // 如果目录有子目录，处理子目录
        if (category.children && category.children.length > 0) {
          const specificChild = childComponents.value[category.id];
          // console.log("进入子目录", specificChild);
          if (specificChild) {
            // console.log("temp1", temp);
            temp = specificChild.checkCategories(); // 确保子组件方法可用
            // console.log("temp2", temp);
            if (temp && temp !== -1) {
              result = temp;
            }
          }
        }
        // console.log("每次返回的result", result);
      }
    }
  });
  return result;
};

// 监听 jumpRoot
watch(
  () => props.jumpRoot,
  (newJumpRoot) => {
    // console.log(newJumpRoot);
    if (newJumpRoot && props.categories.some(category => category.id === newJumpRoot)) {
    // if (newJumpRoot) {
      scrollToCategory(newJumpRoot); // 滚动到对应分类
    }
  }
);

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

.clickable {
  cursor: pointer;
  transition: all 0.3s ease; /* 平滑过渡 */
}

.clickable:hover {
  font-size: 1.1em; /* 略微增大字体 */
  color: #007bff; /* 修改字体颜色 */
  border-bottom: 2px solid #007bff; /* 添加下边框 */
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
  