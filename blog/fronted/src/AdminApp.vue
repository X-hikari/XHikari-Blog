<template>
  <div class="container">
    <!-- 控制按钮列表 -->
    <div class="button-list">
      <button @click="currentView = adminMessageComponent" class="firstbtn">信息管理</button>
      <button @click="showArticleButtons = !showArticleButtons" class="firstbtn">文章管理</button>
      <!-- 文章管理按钮 -->
      <div v-if="showArticleButtons" class="secondbtn-section">
        <button @click="currentView = articleListComponent" class="secondbtn">文章列表</button>
        <button @click="currentView = articlePostComponent; mode = 'create'" class="secondbtn">发布文章</button>
      </div>
      <button class="firstbtn">分类管理</button>
    </div>

    <!-- 动态组件显示 -->
    <div class="component-display">
      <component
        :is="currentView"
        @updateView="updateCurrentView"
        :mode="mode"
        :articleData="mode === 'edit' ? articleData : undefined" />
    </div>
  </div>
</template>

<script setup>
import { ref, markRaw } from 'vue';
import adminMessage from './adminPage/views/adminmessage/adminMessage.vue';
import articlePost from './adminPage/views/adminarticle/articlePost.vue';
import articleList from './adminPage/views/adminarticle/articleList.vue';

const adminMessageComponent = markRaw(adminMessage);
const articlePostComponent = markRaw(articlePost);
const articleListComponent = markRaw(articleList);

const currentView = ref(adminMessage);
const showArticleButtons = ref(false);
const mode = ref('create'); // 默认模式为创建文章
const articleData = ref({}); // 用于存储文章数据的字典

// 更新 currentView 的函数
const updateCurrentView = (viewName, data) => {
  if (viewName === 'articlePost') {
    currentView.value = articlePostComponent;
    mode.value = 'create';
  }
  if (viewName === 'articleEdit') {
    currentView.value = articlePostComponent;
    mode.value = 'edit';
    articleData.value = data;
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.container {
  display: flex;
  width: 100vw;
}

.button-list {
  width: 15%;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.firstbtn {
  padding: 10px;
  text-align: left;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  background-color: white;
  color: grey;
  cursor: pointer;
}

.firstbtn:hover {
  background-color: #f0f0f0;
}

.secondbtn-section {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.secondbtn {
  padding: 10px;
  padding-left: 25px;
  font-size: 14px;
  text-align: left;
  border: none;
  border-radius: 4px;
  background-color: white;
  color: grey;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.secondbtn:hover {
  background-color: #f0f0f0;
}

.component-display {
  flex: 1;
  padding: 20px;
  margin: 0 auto;
  width: 100%;
}
</style>
