<template>
  <div class="webmaster-container">
    <!-- 头像容器 -->
    <div class="avatar-section">
      <img class="avatar" :src="avatarUrl" alt="博主头像" />
      <!-- 更改头像按钮 -->
      <button class="change-avatar-btn" @click="changeAvatar">更改头像</button>
    </div>

    <!-- 其他博主信息 -->
    <div class="info-section">
      <div class="info-item">
        <label for="adminName">博主名称：</label>
        <input id="adminName" type="text" v-model="adminName" />
      </div>
      <div class="info-item">
        <label for="adminSign">个人标签：</label>
        <input id="adminSign" type="text" v-model="adminSign" />
      </div>
      <div class="info-item">
        <label for="adminBackground">背景图片：</label>
        <div class="background-section">
          <button class="change-background-btn" @click="fileInput.click()">修改背景</button>
          <input ref="fileInput" type="file" accept="image/*" @change="handleBackgroundChange" style="display: none;" />
        </div>
      </div>
      <!-- 图片预览 -->
      <div v-if="backgroundUrl" class="preview-section">
        <p>背景预览：</p>
        <img :src="backgroundUrl" alt="背景预览" class="background-preview" />
      </div>
    </div>

    <!-- 相关链接 -->
    <div class="Linkheader">相关链接</div>
    <div class="link-section">
      <div class="info-item">
        <label for="GithubLink">Github：</label>
        <input id="GithubLink" type="text" v-model="GitHubLink" />
      </div>
      <div class="info-item">
        <label for="BilibiliLink">Bilibili：</label>
        <input id="BilibiliLink" type="text" v-model="BilibiliLink" />
      </div>
    </div>

    <!-- 保存和重置按钮 -->
    <div class="action-buttons">
      <button class="save-btn" @click="saveChanges">保存</button>
      <button class="reset-btn" @click="resetChanges">重置</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 响应式变量
const avatarUrl = ref("/UserCard/avatar_xhikari.png"); // 默认头像
const adminName = ref("小肖");
const adminSign = ref("学不动了、学不懂了、学不会了");
const GitHubLink = ref("https://github.com/X-hikari/");
const BilibiliLink = ref("https://space.bilibili.com/505788992");
const backgroundUrl = ref("/UserCard/background.jpg"); // 背景 URL
const fileInput = ref(null); // 文件输入框的引用

// 更改头像的逻辑
function changeAvatar() {
  const newUrl = prompt("请输入新的头像 URL:");
  if (newUrl) {
    avatarUrl.value = newUrl; // 更新头像 URL
  }
}

// 处理背景图片上传
function handleBackgroundChange(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = () => {
      backgroundUrl.value = reader.result; // 更新背景图片
    };
    reader.readAsDataURL(file);
  }
}

// 初始状态备份，用于重置
const initialState = {
  avatarUrl: avatarUrl.value,
  adminName: adminName.value,
  adminSign: adminSign.value,
  GitHubLink: GitHubLink.value,
  BilibiliLink: BilibiliLink.value,
  backgroundUrl: backgroundUrl.value,
};

// 保存更改
function saveChanges() {
  alert("修改已保存！");
  console.log("当前状态", {
    avatarUrl: avatarUrl.value,
    adminName: adminName.value,
    adminSign: adminSign.value,
    GitHubLink: GitHubLink.value,
    BilibiliLink: BilibiliLink.value,
    backgroundUrl: backgroundUrl.value,
  });
}

// 重置更改
function resetChanges() {
  avatarUrl.value = initialState.avatarUrl;
  adminName.value = initialState.adminName;
  adminSign.value = initialState.adminSign;
  GitHubLink.value = initialState.GitHubLink;
  BilibiliLink.value = initialState.BilibiliLink;
  backgroundUrl.value = initialState.backgroundUrl;
  alert("已重置为初始状态！");
}
</script>

<style scoped>
.webmaster-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
  margin: 0 auto;
  width: 80%;
}

.avatar-section {
  position: relative;
  margin-bottom: 20px;
}

.avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ddd;
}

.change-avatar-btn {
  position: absolute;
  bottom: 10px;
  right: -25px;
  padding: 5px 10px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.change-avatar-btn:hover {
  background-color: #0056b3;
}

.info-section {
  width: 100%;
}

.info-item {
  display: flex;
  flex-direction: row;
  margin-bottom: 15px;
  align-items: center;
}

.info-item label {
  width: 120px;
  font-size: 14px;
  font-weight: bold;
  margin-right: 10px;
  color: #333;
}

.info-item input {
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
}

.info-item input:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.background-section {
  width: 100%;
  display: inline-flex;
  align-items: center;
}

.change-background-btn {
  padding: 5px 10px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  background-color: #28a745;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.change-background-btn:hover {
  background-color: #218838;
}

.preview-section {
  margin-top: 20px;
  text-align: center;
}

.background-preview {
  /* width: 100%; */
  height: 200px;
  object-fit: contain;
  border-radius: 8px;
  border: 2px solid #ddd;
}

.Linkheader {
  margin-top: 30px;
  font-size: 1.2em;
  align-items: center;
}

.link-section {
  width: 100%;
}

/* 新增按钮样式 */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px; /* 按钮间距 */
  margin-top: 30px;
}

.save-btn,
.reset-btn {
  padding: 5px 10px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.save-btn {
  background-color: #007bff;
  color: white;
}

.save-btn:hover {
  background-color: #0056b3;
}

.reset-btn {
  background-color: #dc3545;
  color: white;
}

.reset-btn:hover {
  background-color: #c82333;
}
</style>
