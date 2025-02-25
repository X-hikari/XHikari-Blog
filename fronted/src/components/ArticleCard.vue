<template>
  <div class="article-card">
    <!-- 图片部分，如果 imageSrc 不为空才显示 -->
    <div v-if="imageSrc" class="article-card__image">
      <img :src="imageSrc" alt="Article Image" :class="{ 'expanded': isImageExpanded }" ref="imageElement" @load="onImageLoad" />
      <!-- 只有图片实际高度大于200px时才显示展开按钮 -->
      <div v-if="imageHeight > 200 && !isImageExpanded" class="image-down-overlay" @click="expandImage">
        <div class="icon-circle">
          <i class="iconfont icon-arrow-down-s-line"></i>
        </div>
      </div>
      <div v-if="isImageExpanded" class="image-up-overlay" @click="expandImage">
        <div class="icon-circle">
          <i class="iconfont icon-arrow-up-s-line"></i>
        </div>
      </div>
    </div>
    
    <!-- 内容部分 -->
    <div class="article-card__content">
      <h3 class="article-card__title">{{ title }}</h3>
      <p class="article-card__summary" :class="{ expanded: isSummaryExpanded }" ref="summaryElement">
        {{ summary }}
      </p>
      <!-- 只有摘要高度大于60px时才显示展开按钮 -->
      <div v-if="summaryHeight > 60 && !isSummaryExpanded" class="summary-down-overlay" @click="expandSummary">
        <div class="icon-circle">
          <i class="iconfont icon-arrow-down-s-line"></i>
        </div>
      </div>
      <div v-if="isSummaryExpanded" class="summary-up-overlay" @click="expandSummary">
        <div class="icon-circle">
          <i class="iconfont icon-arrow-up-s-line"></i>
        </div>
      </div>

      <!-- 显示日期和阅读量 -->
      <div class="article-card__footer">
        <span class="article-card__date">{{ formattedDate }}</span>
        <span class="article-card__views">{{ views }} 阅读</span>
      </div>

      <button @click="goToArticle(id)" class="read-more-button">阅读更多</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { format } from 'date-fns';  // 用于格式化日期
import { useRouter } from 'vue-router';

const router = useRouter();

// 接收父组件传入的 props
const props = defineProps({
  id: {
    type: Number,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  summary: {
    type: String,
    required: true
  },
  date: {
    type: String,
    required: true
  },
  views: {
    type: Number,
    required: true
  },
  imageSrc: {
    type: String,
    default: ''  // 允许空字符串作为默认值
  }
});

const isImageExpanded = ref(false);
const isSummaryExpanded = ref(false);
const imageElement = ref(null);
const summaryElement = ref(null);

// 用于存储图片和摘要的实际高度
const imageHeight = ref(0);
const summaryHeight = ref(0);

// 扩展图片显示
const expandImage = () => {
  isImageExpanded.value = !isImageExpanded.value;
};

// 扩展摘要显示
const expandSummary = () => {
  isSummaryExpanded.value = !isSummaryExpanded.value;
};

// 跳转到文章详情
const goToArticle = (id) => {
  // 使用 Vue Router 的编程式导航
  router.push({ path: '/article', query: { id } });
};

// 格式化日期
const formattedDate = format(new Date(props.date), 'yyyy年MM月dd日 HH:mm:SS');

// 获取图片和摘要的实际高度
const onImageLoad = () => {
  if (imageElement.value) {
    imageHeight.value = imageElement.value.naturalHeight; // 获取图片的自然高度
  }
};

onMounted(() => {
  nextTick(() => {
    if (summaryElement.value) {
      summaryHeight.value = summaryElement.value.scrollHeight;
    }
  });
});
</script>

<style scoped>
.article-card {
  width: 100%;
  min-width: 720px;
  max-width: 980px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: default;
}

.article-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}

/* 图片部分的样式 */
.article-card__image {
  position: relative;
  width: 100%;
  height: auto;
  overflow: hidden;
}

.article-card__image img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  transition: height 0.3s ease;
  object-position: top;
}

.article-card__image img.expanded {
  height: auto;
}

/* 控制图片展开的按钮 */
.image-down-overlay,
.image-up-overlay {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  cursor: pointer;
}

.image-down-overlay {
  top: 80%;
}

.image-up-overlay {
  bottom: 5%;
}

/* 摘要部分 */
.summary-down-overlay,
.summary-up-overlay {
  left: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  top: 80%;
}

.icon-circle {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.6);
  border-radius: 50%;
  padding: 3px;
}

.icon-circle i {
  color: white;
  font-size: 1em;
}

.article-card__content {
  padding: 15px;
}

.article-card__title {
  font-size: 1.2em;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}

.article-card__summary {
  font-size: 1em;
  color: #777;
  margin-bottom: 15px;
  height: auto;
  max-height: 60px;
  overflow: hidden;
  transition: height 0.3s ease;
}

.article-card__summary.expanded {
  max-height: none;
  overflow: visible;
}

/* 底部内容 */
.article-card__footer {
  display: flex;
  justify-content: space-between;
  font-size: 0.9em;
  color: #aaa;
}

.article-card__footer .article-card__date {
  font-weight: bold;
}

.article-card__footer .article-card__views {
  font-style: italic;
}

.read-more-button {
  padding: 10px;
  background-color: #5e3c3c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.read-more-button:hover {
  background-color: #4a2b2b;
}
</style>
