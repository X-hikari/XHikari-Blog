<template>
  <div class="article">
    <div class="main-content">
      <div class="left-part">
        <div class="sticky-header">
          <Catalogues 
            :directories="headings"
            :activeRoot="activeRoot"
            :parentId="parentId"      
            @update-jump-root="updateJumpRoot"
          />
        </div>
      </div>
      <div class="right-part">
        <ArticleDetailCard v-if="article"
         :data="article"
         :jumpRoot="jumpRoot"
         @update-active-root="updateActiveRoot" />
      </div>
    </div>
  </div>
</template>

<script setup>
const name = 'Article';
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router'; // 用于获取路由参数
import Catalogues from '@/components/Catalogues/Catalogues.vue';
import ArticleDetailCard from '@/components/ArticleDetailCard.vue';
import MarkdownIt from 'markdown-it';

const route = useRoute();
const articleId = ref(route.query.id); // 获取 URL 中的 id 参数

const article = ref(null); // 存储文章数据
const md = new MarkdownIt();
const headings = ref([]);
const jumpRoot = ref(null);
const activeRoot = ref(null); // 当前根目录
const parentId = ref([]);

// 更新当前根目录
const updateActiveRoot = (rootId) => {
  activeRoot.value = rootId;
  const result = findParentIdByActiveRoot(headings.value, activeRoot.value);
  parentId.value = result;
  // console.log("parentId", parentId.value);
};

// 更新当前跳转目录
const updateJumpRoot = (rootId) => {
  jumpRoot.value = rootId;
  // console.log(jumpRoot.value);
  // console.log("parentId", parentId.value);
};

async function fetchArticle(id) {
  axios.get(`http://localhost:8001/api/article?id=${id}`)
  .then(response => {
    article.value = response.data;
    headings.value = parseMarkdownWithHeadings(article.value.content);
    console.log(headings.value);
  })
  .catch(error => {
    console.error('Error fetching article:', error);
  });
}

// 初次加载时调用
onMounted(() => {
  if (articleId.value) {
    fetchArticle(articleId.value);
  };
});

function findParentIdByActiveRoot(headings, activeRoot) {
  // 遍历所有标题
  for (const heading of headings) {
    // 如果找到了目标标题，返回它的 parentId
    if (heading.id === activeRoot) {
      return heading.parentId;
    }

    // 如果当前标题有子标题，递归查找
    if (heading.children.length > 0) {
      const parentId = findParentIdByActiveRoot(heading.children, activeRoot);
      if (parentId) {
        return parentId;
      }
    }
  }
  // 如果没有找到对应的标题，返回 null
  return null;
}

function parseMarkdownWithHeadings(markdownText) {
  // 使用 markdown-it 解析 Markdown 内容
  const tokens = md.parse(markdownText, {});
  const headings = [];
  const stack = [];
  let idCounter = 1;  // 用于生成 ID

  console.log("init", stack);

  tokens.forEach((token, index) => {
    // 如果遇到标题 token
    if (token.type === 'heading_open' && token.tag === 'h1') {
      return ;
    }

    if (token.type === 'heading_open') {
      const level = parseInt(token.tag.slice(1), 10);  // 获取标题的级别
      const nextToken = tokens[index + 1];  // 获取下一个 token，通常是标题的文本内容
      const content = nextToken ? nextToken.content : '';  // 获取标题内容

      const currentId = idCounter++;  // 为当前标题生成唯一的 ID

      // 获取当前标题的父标题 ID，父标题是栈中所有比当前标题级别小的标题
      const parentIds = stack.filter(item => item.level < level).map(item => item.id);

      const heading = {
        id: currentId,        // 当前标题的 ID
        name: content,     // 当前标题的文本内容
        level: level,         // 当前标题的层级
        parentId: parentIds,     // 当前标题的父标题 ID 列表
        children: []          // 子标题数组初始化为空
      };
      
      // 弹出栈中所有不再是父标题的栈元素
      while (stack.length > 0 && stack[stack.length - 1].level >= level) {
        stack.pop();
      }

      // 如果当前标题有父标题，则将当前标题添加到父标题的 children 中
      if (stack.length > 0 && stack[stack.length - 1].level < level) {
        stack[stack.length - 1].children.push(heading);
      } else {
        // 如果没有父标题，则添加到根标题数组中
        console.log(heading, stack.length);
        headings.push(heading);
      }

      // 将当前标题压入栈中，作为后续标题的父标题
      stack.push(heading);
    }
  });
  // console.log(headings.values);

  return headings;  // 返回解析后的标题结构
}

// 监听路由参数变化（支持从 /article?id=1 跳转到 /article?id=2）
watch(
  () => route.query.id,
  (newId) => {
    if (newId) fetchArticle(newId);
  }
);
</script>

<style scoped>
.article {
  display: flex;
  justify-content: center;
  padding-left: 10%;
  padding-right: 10%;
}

.main-content {
  display: flex;
  align-items: stretch;
  width: 100%; /* 剩余部分 */
  gap: 5%;
  align-items: flex-start; /* 确保左、右部分高度独立 */
}

.left-part {
  width: 30%; /* 左边部分占据3的比例 */
  position: relative; /* 确保 sticky 能工作 */
  height: 100%; /* 确保左边部分高度足够 */
}

.sticky-header {
  position: -webkit-sticky; /* Safari 支持的前缀 */
  position: sticky;
  top: 50px; /* 设置距离页面顶部的固定距离 */
  padding: 10px;
}

.right-part {
  width: 70%; /* 右边部分占据7的比例 */
  height: 100%;
  margin-bottom: 1000px;
}
</style>