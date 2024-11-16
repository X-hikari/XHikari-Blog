<template>
  <div class="classifycard">
    <div class="title">文章总览</div>
    <div class="introduce">文章分类如下，点击可以跳转</div>
    <div class="section" ref="section">
      <ul>
        <li v-for="(category, index) in categories" :key="category.id" ref="categoryItems">
          <div>
            <span class="parentclassify">{{ category.name }}</span>
            <div class="articlenumber">共 {{ category.article_count }} 篇</div>
          </div>

          <!-- 递归渲染子分类 -->
          <ClassifyItem 
            v-if="category.children && category.children.length > 0" 
            :categories="category.children"
            :ref="el => { if (el) childComponents[category.id] = el; }"
          />
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import ClassifyItem from '@/components/Classify/ClassyItem.vue';
import { eachMinuteOfInterval } from 'date-fns';

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

// 滚动事件处理函数
const handleScroll = () => {
  const checkCategories = (categories, categoryItems) => {
    // 遍历当前目录
    categories.forEach((category, index) => {
      const el = categoryItems.value[index]; // 获取对应的 DOM 元素
      if (el) {
        const rect = el.getBoundingClientRect();
        // 如果该目录项在视口内
        if (rect.top <= buffer) {
          emit('update-active-root', category.id);

          // 如果目录有子目录，处理子目录
          if (category.children && category.children.length > 0) {
            const specificChild = childComponents.value[category.id];
            console.log("进入子目录", specificChild);
            if (specificChild) {
              const result = specificChild.checkCategories(); // 确保子组件方法可用
              console.log("最外层的result", result);
              if (result !== -1) {
                emit('update-active-root', result);
                console.log("fin", result);
              }
            }
          }
        }
      }
    });
  };

  // 调用函数，传入顶层目录（props.categories）
  checkCategories(props.categories, categoryItems);
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
.classifycard {
  width: 100%;
  background-color: rgba(251, 248, 247, 0.8);
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  padding: 20px;
  backdrop-filter: blur(1px);
  margin-bottom: 1000px;
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

ul {
  padding-left: 10px;
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
  display: block;
  font-size: 0.7em;
  font-weight: bold;
  color: white;
  background-color: #4fa3f7;
  padding: 2.5px 15px;
  border-radius: 6px;
  text-align: center;
  margin-top: 10px;
  margin-bottom: 5px;
  width: fit-content;
}
</style>