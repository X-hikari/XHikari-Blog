<template>
  <div class="article-card">
    <div class="article-card__image">
      <img :src="imageSrc" alt="Article Image" :class="{ 'expanded': isImageExpanded }" ref="imageElement" />
      <div v-if="!isImageExpanded" class="image-down-overlay" @click="expandImage">
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
    <div class="article-card__content">
      <h3 class="article-card__title">{{ title }}</h3>
      <p class="article-card__summary" :class="{ expanded: isSummaryExpanded }">
        {{ summary }}
      </p>
      <div v-if="!isSummaryExpanded" class="summary-down-overlay" @click="expandSummary">
        <div class="icon-circle">
          <i class="iconfont icon-arrow-down-s-line"></i>
        </div>
      </div>
      <div v-if="isSummaryExpanded" class="summary-up-overlay" @click="expandSummary">
        <div class="icon-circle">
          <i class="iconfont icon-arrow-up-s-line"></i>
        </div>
      </div>
      <div class="article-card__footer">
        <span class="article-card__date">{{ date }}</span>
        <span class="article-card__views">{{ views }} 阅读</span>
      </div>
      <button @click="goToArticle" class="read-more-button">阅读更多</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const title = "文章测试";
const summary = "这是博客文章的摘要？或者内容前部分？命运石之门 椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理椎名真由理";
const date = "2024年11月11日";
const views = 142;
const imageSrc = "/homeBackground.jpg"; // 图片路径

const isImageExpanded = ref(false);
const isSummaryExpanded = ref(false);
const imageElement = ref(null);

const expandImage = () => {
  isImageExpanded.value = !isImageExpanded.value;
};

const expandSummary = () => {
  isSummaryExpanded.value = !isSummaryExpanded.value;
};

const goToArticle = () => {
  alert("跳转到文章详情页面");
};
</script>

<style scoped>
.article-card {
  width: 100%;
  max-width: 980px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.article-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}

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

.summary-down-overlay,
.summary-up-overlay {
  left: 50%;  /* 初始位置居中 */
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  top: 80%;
}

.icon-circle {
  display: inline-flex; /* 使用 inline-flex 来支持内容居中 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  background-color: rgba(0, 0, 0, 0.6);
  border-radius: 50%;
  padding: 3px; /* 缩小圆形外框 */
}

.icon-circle i {
  color: white;
  font-size: 1em; /* 缩小图标大小 */
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
  height: 60px;  /* 默认高度限制 */
  overflow: hidden;  /* 内容溢出时隐藏 */
  transition: height 0.3s ease;  /* 平滑过渡 */
}

.article-card__summary.expanded {
  height: auto;  /* 展开后高度自适应 */
  overflow: visible;  /* 展开后内容可见 */
}

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
