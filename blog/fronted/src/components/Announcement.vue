<template>
    <div class="announcement-bar">
      <div class="announcement-title">
        <i class="iconfont icon-gonggao"></i>
        <span>{{ title }}</span>
      </div>
      <div class="announcement-content">
        <p>{{ content }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const title = "公告栏";
  const content = "这里是公告栏喵！";
  </script>
  
  <style scoped>
  .announcement-bar {
    width: 100%;
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  
  .announcement-title {
    padding: 5%;
    padding-bottom: 2%;
    display: flex;
    align-items: center;
    font-size: 1.2em;
    color: #333;
  }
  
  .announcement-title .iconfont {
    font-size: 1.5em;
    margin-right: 10px;
    /* color: #007bff; 图标颜色 */
  }
  
  .announcement-content {
    padding: 5%;
    padding-top: 0;
    font-size: 1em;
    color: #555;
  }
  </style>
  