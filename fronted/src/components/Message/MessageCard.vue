<template>
  <div class="overlay" @click="closeMessage">
    <div class="message-card" @click.stop>
      <p class="message-content">{{ message.content }}</p>
      <div class="info">
        <p class="user">用户：{{ message.user }}</p>
        <p class="created-at">留言时间：{{ formattedTime }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  message: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(["close"]);

const formattedTime = computed(() => {
  const utcDate = new Date(props.message.created_at); // 转换为 Date 对象
  return utcDate.toLocaleString("zh-CN", { timeZone: "Asia/Shanghai" });
});

// 关闭留言卡片
const closeMessage = () => {
  emit("close");
};
</script>

<style scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7); /* 遮罩层，背景为半透明黑色 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  /* cursor: pointer; */
}

.message-card {
  background: #f8f0c2; /* 纸张背景色 */
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 0 40px rgba(0, 0, 0, 0.5); /* 增加阴影效果 */
  width: 80vw;
  max-width: 700px; /* 最大宽度控制 */
  text-align: left;
  font-family: "Arial", sans-serif;
  position: relative;
  cursor: default;
  overflow: hidden; /* 保证文本不会溢出纸张 */
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* 保证内容区域从上到下排列 */
}

.message-content {
  font-size: 16px;
  font-weight: 400;
  word-wrap: break-word;
  white-space: pre-wrap;
  margin-bottom: 10px;
  line-height: 24px; /* 设置行高为24px */
  background-image: linear-gradient(to bottom, transparent 23px, #333 23px, #333 24px, transparent 24px);
  background-size: 100% 24px;
  background-repeat: repeat-y;
  padding-bottom: 1px; /* 确保最后一行下方也有横线 */
}

.info {
  font-size: 14px;
  color: #888;
  margin-top: 10px;
}

.user,
.created-at {
  margin: 0;
  font-size: 14px;
}
</style>
