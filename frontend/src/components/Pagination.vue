<!-- components/Pagination.vue -->
<template>
  <div class="pagination">
    <button @click="changePage(page - 1)" :disabled="page <= 1">上一页</button>
    <span class="PageText">{{ page }} / {{ totalPages }}</span>
    <button @click="changePage(page + 1)" :disabled="page >= totalPages">下一页</button>
  </div>
</template>
  
<script setup>
// 接收父组件传递的参数
const props = defineProps({
page: {
  type: Number,
  required: true
},
totalPages: {
  type: Number,
  required: true
}
});

// 用于发送改变页面的事件
const emit = defineEmits(['changePage']);

// 改变当前页
const changePage = (newPage) => {
if (newPage >= 1 && newPage <= props.totalPages) {
  emit('changePage', newPage);
}
};
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination button {
  padding: 10px 20px;
  background-color: #5e3c3c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 0 10px;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.PageText {
  font-size: 20px;
}
</style>
  