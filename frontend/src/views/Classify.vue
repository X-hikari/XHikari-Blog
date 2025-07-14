<template>
  <div class="classify">
    <div class="main-content">
      <div class="left-part">
        <div class="sticky-header">
          <Catalogues 
            :directories="categorys"
            :activeRoot="activeRoot"
            :parentId="parentId"      
            @update-jump-root="updateJumpRoot"
          />
        </div>
      </div>
      <div class="right-part">
        <ClassifyCard 
          :categories="categorys"
          :jumpRoot="jumpRoot"
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
const parentId = ref([]);
const jumpRoot = ref(null);
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

function findCategoryById(data, targetId) {
  for (const item of data) {
    if (item.id === targetId) {
      return item; // 找到目标 ID，返回对应的目录对象
    }
    // 如果有子节点，递归搜索子节点
    if (item.children && item.children.length > 0) {
      const result = findCategoryById(item.children, targetId);
      if (result) {
        return result; // 如果在子节点中找到，直接返回结果
      }
    }
  }
  return null; // 如果找不到，返回 null
}

// 更新当前根目录
const updateActiveRoot = (rootId) => {
  // alert(rootId);
  activeRoot.value = rootId;
  const result = findCategoryById(categorys.value, activeRoot.value);
  parentId.value = result.parent;
  // console.log("parentId", parentId.value);
};

// 更新当前跳转目录
const updateJumpRoot = (rootId) => {
  jumpRoot.value = rootId;
  // console.log(jumpRoot.value);
  // console.log("parentId", parentId.value);
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
  align-items: flex-start;
  width: 100%;
  max-width: 1200px;
  gap: 5%;
}

.left-part {
  width: 30%;
  position: relative;
}

.sticky-header {
  position: sticky;
  top: 50px;
  padding: 10px;
}

.right-part {
  width: 65%;
  margin-bottom: 1000px;
}

/* 响应式样式：小屏幕堆叠布局 */
@media screen and (max-width: 768px) {
  .main-content {
    flex-direction: column;
    gap: 20px;
  }

  .left-part,
  .right-part {
    width: 100%;
  }

  .sticky-header {
    position: relative; /* sticky在小屏时可能不适合，改为普通流 */
    top: 0;
  }
}
</style>