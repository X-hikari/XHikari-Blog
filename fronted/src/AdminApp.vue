<template>
  <div class="container">
    <!-- 控制按钮列表 -->
    <div class="button-list">
      <button @click="addTab('信息管理', adminMessageComponent)" class="firstbtn">信息管理</button>
      <button @click="showArticleButtons = !showArticleButtons" class="firstbtn">文章管理</button>
      <!-- 文章管理按钮 -->
      <div v-if="showArticleButtons" class="secondbtn-section">
        <button @click="addTab('文章列表', articleListComponent)" class="secondbtn">文章列表</button>
        <button @click="addTab('发布文章', articlePostComponent, 'create')" class="secondbtn">发布文章</button>
      </div>
      <button @click="addTab('分类管理', categoryListComponent)" class="firstbtn">分类管理</button>
      <button @click="showAlbumButtons = !showAlbumButtons" class="firstbtn">相册管理</button>
      <div v-if="showAlbumButtons" class="secondbtn-section">
        <button @click="addTab('相片管理', albumPhotoList)" class="secondbtn">相片管理</button>
        <button @click="addTab('相册管理', albumList)" class="secondbtn">相册管理</button>
      </div>
    </div>

    <!-- 动态组件和顶部标签页 -->
    <div class="content-area">
      <!-- 顶部标签页 -->
      <div class="tabs">
        <div
          v-for="(tab, index) in tabs"
          :key="index"
          :class="['tab', currentTabIndex === index ? 'active' : '']"
        >
          <span @click="currentTabIndex = index">{{ tab.title }}</span>
          <button class="close-btn" @click="closeTab(index)">x</button>
        </div>
      </div>

      <!-- 动态组件显示 -->
      <div class="component-display">
        <component
          v-if="tabs.length"
          :is="tabs[currentTabIndex]?.component"
          :key="currentTabIndex"
          @updateView="updateCurrentView"
          :mode="tabs[currentTabIndex]?.mode"
          :articleData="tabs[currentTabIndex]?.articleData"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, markRaw } from 'vue';
import adminMessage from './adminPage/views/adminmessage/adminMessage.vue';
import articlePost from './adminPage/views/adminarticle/articlePost.vue';
import articleList from './adminPage/views/adminarticle/articleList.vue';
import categoryList from './adminPage/views/admincategory/categoryList.vue';
import albumPhotoList from './adminPage/views/adminalbum/albumPhotosList.vue';
import albumList from './adminPage/views/adminalbum/albumList.vue';

const adminMessageComponent = markRaw(adminMessage);
const articlePostComponent = markRaw(articlePost);
const articleListComponent = markRaw(articleList);
const categoryListComponent = markRaw(categoryList);

// 标签页和当前显示的页面
const tabs = ref([]);
const currentTabIndex = ref(0);
const showArticleButtons = ref(false);
const showAlbumButtons = ref(false);

// 添加标签页的函数
const addTab = (title, component, mode = null, articleData = null) => {
  const existingTabIndex = tabs.value.findIndex(tab => 
    tab.title === title && JSON.stringify(tab.articleData) === JSON.stringify(articleData)
  );
  if (existingTabIndex !== -1) {
    // 如果标签页已存在，则切换到该标签页
    currentTabIndex.value = existingTabIndex;
  } else {
    // 如果标签页不存在，则添加
    tabs.value.push({ title, component, mode, articleData });
    currentTabIndex.value = tabs.value.length - 1;
  }
};

// 关闭标签页的函数
const closeTab = (index) => {
  tabs.value.splice(index, 1);
  if (index === currentTabIndex.value) {
    // 如果关闭的是当前标签页，则切换到上一个标签页或第一个标签页
    currentTabIndex.value = index > 0 ? index - 1 : 0;
  } else if (index < currentTabIndex.value) {
    // 如果关闭的是前面的标签页，则当前标签索引减一
    currentTabIndex.value -= 1;
  }
};

// 更新 currentView 的函数
const updateCurrentView = (viewName, data) => {
  if (viewName === 'articlePost') {
    addTab('发布文章', articlePostComponent, 'create');
  }
  if (viewName === 'articleEdit') {
    addTab('编辑文章', articlePostComponent, 'edit', data);
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

/* 内容区域 */
.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  user-select: none;
}

/* 标签页样式 */
.tabs {
  display: flex;
  background-color: #f8f8f8;
  border-bottom: 1px solid #ddd;
  padding: 5px 10px;
}

.tab {
  margin-right: 10px;
  padding: 5px 10px;
  background-color: #e0e0e0;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  user-select: none;
}

.tab.active {
  background-color: #4CAF50;
  color: white;
}

.tab:hover {
  background-color: #d0d0d0;
}

.close-btn {
  margin-left: 5px;
  background: none;
  border: none;
  color: grey;
  cursor: pointer;
  font-size: 14px;
  user-select: none;
}

.close-btn:hover {
  color: rgb(63, 63, 63);
}

.component-display {
  flex: 1;
  padding: 20px;
  margin: 0 auto;
  width: 100%;
}
</style>
