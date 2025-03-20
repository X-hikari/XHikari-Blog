<template>
  <div class="website-info">
    <h2>网站信息</h2>
    <ul>
      <li class="info-item">
        <span class="info-label">运行时间:</span>
        <p class="info-value">{{ runTime }}</p>
      </li>
      <li class="info-item">
        <span class="info-label">今日访问:</span>
        <p class="info-value">{{ todayvisit }}</p>
      </li>
      <li class="info-item">
        <span class="info-label">累计访问:</span>
        <p class="info-value">{{ visitCount }}</p>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from "axios";

// 文章数目
const todayvisit = ref(0);
// 运行时间，这里用天数表示
const creTime = ref("2024-12-18 21:58:37");
const startTime = new Date(creTime.value).getTime(); // 获取当前时间（单位：毫秒）
const runTime = ref('0 天 0 小时 0 分钟 0 秒');
// 博客访问次数
const visitCount = ref(0);

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

const fetchWebInformation = async () => {
  const response = await axios.get("http://localhost:8001/api/webinformation/");
  if (response.status == 200){
    visitCount.value = response.data.total_views;
    todayvisit.value = response.data.today_views;
  }
}

onMounted(() => {
  fetchWebInformation();
  setInterval(updateRunTime, 1000); // 每秒调用一次
});
</script>

<style scoped>
.website-info {
  width: 100%;
  max-width: 600px;
  /* margin: auto; */
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
  