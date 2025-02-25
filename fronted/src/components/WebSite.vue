<template>
    <div class="website-info">
      <h2>网站信息</h2>
      <ul>
        <li class="info-item">
          <span class="info-label">运行时间:</span>
          <span class="info-value">{{ runtime }}</span>
        </li>
        <li class="info-item">
          <span class="info-label">今日访问:</span>
          <span class="info-value">{{ todayvisit }}</span>
        </li>
        <li class="info-item">
          <span class="info-label">累计访问:</span>
          <span class="info-value">{{ visitCount }}</span>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  // 文章数目
  const todayvisit = ref(38000);
  // 运行时间，这里用天数表示
  const runtime = ref(22595);
  // 博客访问次数
  const visitCount = ref('38000');
  </script>
  
  <style scoped>
  .website-info {
    width: 100%;
    max-width: 600px;
    margin: auto;
    padding: 20px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .website-info h2 {
    text-align: left;
    margin-bottom: 20px;
    font-size: 1.5em;
  }
  
  ul {
    list-style-type: disc; /* 显示小圆点 */
    padding-left: 20px; /* 增加左侧内边距，使圆点不被遮挡 */
    margin: 0;
  }
  
  .info-item {
    margin-bottom: 10px;
  }
  
  .info-label {
    font-weight: bold;
  }
  
  .info-value {
    margin-left: 10px;
    font-size: 1.2em;
    color: #333;
  }
  </style>
  