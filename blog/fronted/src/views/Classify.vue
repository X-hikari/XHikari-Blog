<template>
  <div class="classify">
    <div class="main-content">
      <div class="left-part">
        <div class="sticky-header">
          <Catalogues 
            :directories="categorys"
            :activeRoot="activeRoot"      
          />
        </div>
      </div>
      <div class="right-part">
        <ClassifyCard 
          :categories="categorys"
          @update-active-root="updateActiveRoot"
          />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import ClassifyCard from '@/components/Classify/ClassifyCard.vue';
import Catalogues from '@/components/Catalogues/Catalogues.vue';

const name = 'Classify';
const categorys = ref([]);
const activeRoot = ref(null); // 当前根目录

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

// 更新当前根目录
const updateActiveRoot = (rootId) => {
  // alert(rootId);
  activeRoot.value = rootId;
};

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
  position: relative; /* 确保 sticky 能工作 */
  height: 100vh; /* 确保左边部分高度足够 */
}

.sticky-header {
  position: -webkit-sticky; /* Safari 支持的前缀 */
  position: sticky;
  top: 50px; /* 设置距离页面顶部的固定距离 */
  padding: 10px;
}


.right-part {
  width: 65%; /* 右边部分占据7的比例 */
}
</style>