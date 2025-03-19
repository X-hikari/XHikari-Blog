<template>
  <div class="webinformation-container">
    <!-- 网站基础信息 -->
    <div class="head">网站基础信息</div>
    <div class="base-section">
      <div class="info-item">
        <label for="webName">网站名称：</label>
        <input id="webName" type="text" v-model="webName" />
      </div>
      <div class="info-item">
        <label for="webSign">入站标语：</label>
        <textarea id="webSign" v-model="webSign" rows="4" placeholder="请输入标语"></textarea>
      </div>
      <div class="info-item">
        <label for="webBulletin">入站公告：</label>
        <textarea id="webBulletin" v-model="webBulletin" rows="4" placeholder="请输入入站公告"></textarea>
      </div>
      <div class="word-count">
        {{ currentBulletinLength }} / {{ maxBulletinLength }} 字
      </div>
    </div>

    <!-- 网站资讯 -->
    <div class="head">网站资讯</div>
    <div class="unmodifiable-section">
      <div class="unmodifiable-info-item">
        <label for="runTime">运行时长：</label>
        <input id="runTime" type="text" v-model="runTime" disabled/>
      </div>
      <div class="unmodifiable-info-item">
        <label for="creTime">创建时间：</label>
        <input id="creTime" type="text" v-model="creTime" disabled />
      </div>
    </div>
    
    <div class="unmodifiable-section">
      <div class="unmodifiable-info-item">
        <label for="articleNum">文章数目：</label>
        <input id="articleNum" type="text" v-model="articleNum" disabled/>
      </div>
      <div class="unmodifiable-info-item">
        <label for="todayVisit">今日访问：</label>
        <input id="todayVisit" type="text" v-model="todayVisit" disabled/>
      </div>
      <div class="unmodifiable-info-item">
        <label for="totalVisit">总访问量：</label>
        <input id="totalVisit" type="text" v-model="totalVisit" disabled/>
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
import { ref, computed, onMounted } from 'vue';
import axios from "axios";

const webName = ref("Xhikari");
const webSign = ref("与你在此的相遇\n就是命运石之门的选择");
const webBulletin = ref("这里是公告栏喵！这里是小肖的赛博小窝，正在搭建喵！")
const maxBulletinLength = 75;  // 设置公告最大字数
const currentBulletinLength = computed(() => webBulletin.value.length);
const articleNum = ref(0);
const todayVisit = ref(0);
const totalVisit = ref(0);

// 定义初始时间
const creTime = ref("2024-12-18 21:58:37");
const startTime = new Date(creTime.value).getTime(); // 获取当前时间（单位：毫秒）
const runTime = ref(' 0 天 0 小时 0 分钟 0 秒');

// 每秒更新运行时长
const updateRunTime = () => {
  const currentTime = new Date().getTime(); // 当前时间
  const elapsedTime = currentTime - startTime; // 计算时间差（毫秒）

  // 将时间差转换为天、小时、分钟、秒
  const seconds = Math.floor(elapsedTime / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  // 格式化为 "X天X小时X分钟X秒"·
  runTime.value = ` ${days} 天 ${hours % 24} 小时 ${minutes % 60} 分钟 ${seconds % 60} 秒`;
};

const fetchArticleNum = async () => {
  const response = await axios.get("http://localhost:8001/api/admin/searchArticle/");
  articleNum.value = response.data.count;
}

// 组件挂载后启动定时器，每秒更新一次运行时长
onMounted(() => {
  fetchArticleNum();
  setInterval(updateRunTime, 1000); // 每秒调用一次
});

</script>

<style>
.webinformation-container {
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

.head {
  margin-top: 30px;
  margin-bottom: 20px;
  font-size: 1.2em;
  align-items: center;
}

.base-section {
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

.info-item textarea {
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
}

.info-item textarea:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.info-item input:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.word-count {
  font-size: 12px;
  color: #888;
  text-align: right;
}

.unmodifiable-section {
  display: flex;
  width: 100%;
  margin-bottom: 15px;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.unmodifiable-info-item {
  display: flex;
  flex-direction: row;
  margin-bottom: 15px;
  align-items: center;
}

.unmodifiable-info-item label {
  width: 120px;
  font-size: 14px;
  font-weight: bold;
  margin-right: 10px;
  color: #333;
}

.unmodifiable-info-item input {
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
}

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