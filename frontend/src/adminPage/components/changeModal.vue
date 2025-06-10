<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h3 v-if="title">{{ title }}</h3>
        <button class="close-btn" @click="close"> X </button>
      </div>
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, watch } from "vue";

// Props 接收是否显示
const props = defineProps({
  visible: Boolean, // 控制模态显示
  title: {
    type: String,
    default: "", // 默认值为空字符串
  },
});

// Emit 用于通知父组件关闭模态
const emit = defineEmits(["update:visible"]);

// 禁用滚动
function disableScroll() {
  document.body.style.overflow = "hidden";
}

// 恢复滚动
function enableScroll() {
  document.body.style.overflow = "";
}

// 关闭模态窗口
function close() {
  emit("update:visible", false);
}

// 监听 visible 属性，禁用/恢复滚动
watch(
  () => props.visible,
  (newVal) => {
    if (newVal) disableScroll();
    else enableScroll();
  }
);

// 确保组件卸载时恢复滚动
onUnmounted(() => enableScroll());
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  position: relative;
}

.modal-header {
  display: flex;
  justify-content: space-between; /* 标题和按钮两端对齐 */
  align-items: center; /* 垂直居中 */
  margin-bottom: 20px; /* 添加下边距分隔内容 */
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
}

.close-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #333;
  padding: 5px; /* 增加可点击区域 */
}

/* 使用深度选择器让form-item和input样式生效 */
:deep(.form-item) {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  justify-content: center;
}

:deep(.form-item label) {
  width: 100px;
  font-weight: bold;
  margin-right: 20px;
  display: inline-block;
}

:deep(.form-item input),
:deep(.form-item textarea),
:deep(.form-item select) {
  flex: 1;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

:deep(.background-section) {
  flex: 1;
  display: inline-flex;
  align-items: center;
}

:deep(.change-background-btn) {
  padding: 5px 10px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  background-color: #28a745;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

:deep(.change-background-btn:hover) {
  background-color: #218838;
}

:deep(.preview-section) {
  margin-top: 20px;
  text-align: center;
}

:deep(.background-preview) {
  /* width: 100%; */
  max-width: 100%;
  height: 200px;
  object-fit: contain;
  border-radius: 8px;
  border: 2px solid #ddd;
}
</style>
