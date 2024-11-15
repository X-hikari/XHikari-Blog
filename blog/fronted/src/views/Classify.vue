<template>
  <div class="classify">
    <div class="main-content">
      <div class="left-part">
        这是左边部分
      </div>
      <div class="right-part">
        <ClassifyCard 
          :categories="categorys"
          />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import ClassifyCard from '@/components/Classify/ClassifyCard.vue';

const name = 'classify';
const categorys = ref([]);

onMounted(() => {
  // 获取所有分类数据
  axios.get('http://localhost:8001/api/categorys')
    .then(response => {
      categorys.value = response.data;
    })
    .catch(error => {
      console.error('Error fetching categorys:', error);
    });
});

</script>

<style scoped>
.classify {
  display: flex;
  justify-content: center;
  padding-left: 10%;
  padding-right: 10%;
}

.main-content {
  display: flex;
  width: 80%; /* 剩余部分 */
  gap: 5%;
  align-items: flex-start; /* 确保左、右部分高度独立 */
}

.left-part {
  width: 30%; /* 左边部分占据3的比例 */
  background-color: #f0f0f0; /* 仅为示例背景色 */
}

.right-part {
  width: 65%; /* 右边部分占据7的比例 */
}
</style>