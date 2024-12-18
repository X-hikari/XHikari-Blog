<template>
  <div class="user-card">
    <!-- 背景图片区域 -->
    <div class="user-card__cover">
      <img src="/UserCard/background.jpg" alt="Cover Image" class="cover-image" />
      <div class="overlay">
        <img src="/UserCard/avatar_xhikari.png" alt="Avatar" class="avatar" />
        <h3 class="username">小肖的个人博客</h3>
        <p class="status">学不动了、学不懂了、学不会了</p>
      </div>
    </div>

    <!-- 统计数据 -->
    <div class="user-card__stats">
      <div>
        <span>文章 </span>
        <span> 22</span>
      </div>
      <div>
        <span>分类 </span>
        <span> 4</span>
      </div>
      <div>
        <span>标签 </span>
        <span> 22</span>
      </div>
    </div>

    <!-- 社交图标 -->
    <div class="user-card__social-icons">
      <i class="iconfont icon-weixin" @click="handleIconClick('微信')"></i>
      <i class="iconfont icon-QQ" @click="handleIconClick('QQ')"></i>
      <i class="iconfont icon-github-fill" @click="handleIconClick('GitHub')"></i>
      <i class="iconfont icon-bilibili-line" @click="handleIconClick('Bilibili')"></i>
    </div>
  </div>
</template>

<script setup>
const handleIconClick = (platform) => {
  alert(`你点击了 ${platform} 图标`);
}
</script>

<style scoped>
.user-card {
  width: 100%;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  text-align: center;
  font-family: Arial, sans-serif;
}

.user-card__cover {
  position: relative;
}

.cover-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  opacity: 0.8;
}

.overlay {
  position: absolute;
  top: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 3px solid white;
}

.username {
  font-size: 1.2em;
  font-weight: bold;
  margin: 10px 0 5px;
}

.status {
  color: #f0f0f0;
  font-size: 0.9em;
}

.user-card__stats {
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}

.user-card__stats div {
  text-align: center;
}

.user-card__stats span:first-child {
  color: #8b5c5c;
}

.user-card__stats span:last-child {
  font-weight: bold;
}

.user-card__social-icons {
  display: flex;
  justify-content: center;
  gap: 10px;
  padding: 10px 0;
}

.user-card__social-icons i {
  font-size: 1.5em;
  cursor: pointer;
}

.user-card__social-icons i:hover {
  color: #0073e6;
}
</style>
