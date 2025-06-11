<template>
  <div class="articledetail">
    <!-- 文章标题 -->
    <div class="articleDetailTitle">{{ data.title }}</div>

    <!-- 元信息 -->
    <div class="article-meta">
      <!-- 专栏和浏览量 -->
      <div class="meta-row">
        <span v-if="data.category" class="meta-item">
          所属专栏：<strong>{{ data.category }}</strong>
        </span>
        <span class="meta-item" v-if="data.visits" >浏览量：{{ data.visits }} 次</span>
      </div>
      
      <!-- 时间信息 -->
      <div class="meta-row">
        <span class="meta-item" v-if="data.created_at">创建时间：{{ data.created_at }}</span>
        <span class="meta-item" v-if="data.updated_at">更新时间：{{ data.updated_at }}</span>
      </div>
    </div>
    
    <!-- Banner 图（如果有） -->
    <div v-if="data.banner_url" class="article-banner">
      <img :src="`http://localhost:8001${data.banner_url}`" alt="Banner" />
    </div>

    <!-- 摘要（如果有） -->
    <div v-if="data.summary" class="article-summary">
      {{ data.summary }}
    </div>

    <!-- Markdown 内容 -->
    <div class="content markdown-body line-numbers" v-html="htmlContent" ref="markdownContent"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch, onBeforeUnmount } from 'vue';
import MarkdownIt from 'markdown-it';
import Prism from 'prismjs';
import '@/assets/css/markdown-style.css';
import "@/utils/mathjax";
import "mathjax/es5/tex-svg"; 

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  jumpRoot: {
    type: Number,
    required: true
  },
});

const emit = defineEmits(['update-active-root']);
const md = new MarkdownIt({
  html: false,
  linkify: true,
});
const htmlContent = ref('');
const headings = ref([]);
const buffer = 50; // 触发位置距离顶部的缓冲距离

// 语法高亮处理
onMounted(() => {
  Prism.highlightAll();
});

// 解析 markdown 内容并渲染
onMounted(() => {
  // 渲染 markdown 内容为 HTML
  window.MathJax.startup.defaultReady();
  htmlContent.value = md.render(props.data.content);

  // 提取所有标题信息
  const tokens = md.parse(props.data.content, {});
  let idCounter = 1;

  tokens.forEach((token, index) => {
    if (token.type === 'heading_open') {
      const level = parseInt(token.tag.slice(1), 10); // 获取标题的层级
      const nextToken = tokens[index + 1]; // 获取标题文本
      const content = nextToken ? nextToken.content : '';

      const heading = {
        id: idCounter++, // 唯一的 ID
        name: content, // 标题内容
        level: level, // 标题层级
        ref: null, // 预留 ref 用于指向 DOM 元素
      };

      headings.value.push(heading);
    }
  });

  // 在页面渲染完后，动态绑定标题的 ref
  nextTick(() => {
    const markdownContent = document.querySelector('.markdown-body');
    if (markdownContent) {
      const headingElements = markdownContent.querySelectorAll('h2, h3, h4, h5, h6');
      headingElements.forEach((el, index) => {
        headings.value[index].ref = el; // 绑定 ref
      });

      // 重新调用 Prism 高亮
      Prism.highlightAll();
    }
  });
});


// 滚动事件处理函数
const handleScroll = () => {
  headings.value.forEach((heading) => {
    const el = heading.ref; // 获取对应的 DOM 元素
    if (el) {
      const rect = el.getBoundingClientRect();
      if (rect.top <= buffer) {
        emit('update-active-root', heading.id); // 更新活动的目录项
      }
    }
  });
};

// 滚动到指定分类
const scrollToCategory = (categoryId) => {
  nextTick(() => {
    const targetIndex = headings.value.findIndex((heading) => heading.id === categoryId);
    if (targetIndex !== -1 && headings.value[targetIndex]) {
      const targetElement = headings.value[targetIndex].ref;
      const rect = targetElement.getBoundingClientRect();
      const offsetTop = rect.top + window.scrollY;

      // 滚动到目标位置，距离顶部50px
      window.scrollTo({
        top: offsetTop - buffer + 5, // 调整50px
        behavior: 'smooth',  // 平滑滚动
      });
    }
  });
};

// 监听 jumpRoot
watch(
  () => props.jumpRoot,
  (newJumpRoot) => {
    if (newJumpRoot && headings.value.some(heading => heading.id === newJumpRoot)) {
      scrollToCategory(newJumpRoot); // 滚动到对应分类
    }
  }
);

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
.articledetail {
  width: 100%;
  background-color: rgba(251, 248, 247, 0.8);
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  padding: 20px;
  backdrop-filter: blur(1px);
}

.article-banner img {
  width: 100%;
  height: auto;
  max-height: 300px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 10px;
}

.articleDetailTitle {
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

.article-summary {
  font-size: 1em;
  margin: 20px 0;
  color: #555;
  line-height: 1.5;
}

.article-meta {
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

.content {
  margin-top: 20px;
}
</style>
