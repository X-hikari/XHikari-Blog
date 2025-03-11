<template>
  <div class="catalogues">
    <div class="sticky-header">
        <div class="Cataloguestitle">文章目录</div>
        <ul>
        <li v-for="(catalogue, index) in directories" :key="index">
          <span :class="['Text' ,{'active': shouldcolor(catalogue.id)}]" @click="jumpRoot(catalogue.id)">{{ catalogue.name }}</span>
          <!-- 判断是否展开子目录 -->
          <CatalogueItem 
            v-if="shouldExpand(catalogue.id)" 
            :directories="catalogue.children" 
            :activeRoot="activeRoot"
            :parentId="parentId"
            @update-jump-root="updateJumpRoot"     
          />
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import CatalogueItem from '@/components/Catalogues/CatalogueItem.vue';

// 定义组件的 prop
const props = defineProps({
  // directories:数组，每个元素只有id、name、children
  directories: {
    type: Array,
    required: true
  },
  activeRoot: {
    type: Number, // 根目录 ID
    required: false
  },
  parentId: {
    type: Array,
    required: false
  }
});

const emit = defineEmits(['update-jump-root']);
const jumpRoot = (catalogueId) => {
  emit('update-jump-root', catalogueId);
};

const updateJumpRoot = (catalogueId) => {
  emit('update-jump-root', catalogueId);
}

// 判断当前目录是否应该展开
const shouldExpand = (catalogueId) => {
  if( props.activeRoot === catalogueId || props.parentId.includes(catalogueId)) {
    return true;
  }
};

const shouldcolor = (catalogueId) => {
  return props.activeRoot === catalogueId;
}
</script>

<style>
.catalogues {
  width: 100%;
  background-color: rgba(251, 248, 247, 0.8);
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  padding: 20px;
  backdrop-filter: blur(1px);
}

.Cataloguestitle {
  color: #b17fc6;
  position: relative;
  font-size: 1.2em;
  font-weight: bold;
  padding-left: 1em;
  margin-bottom: 0.8em;
}

.Cataloguestitle::before {
  top: 10%;
  content: '';
  position: absolute;
  left: 0;
  width: 5px;
  height: 100%;
  background-color: rgba(145, 196, 238);
  border-radius: 3px;
}

ul {
  padding-left: 10px;
  list-style-type: none;
  color: #34345f
}

.Text {
  display: block;
  width: 100%;
  font-weight: bold;
}

.Text:hover {
  background-color: #e9f3fc;
  cursor: pointer;
}

.active {
  color: rgba(145, 196, 238); /* 当前项的字体颜色为蓝色 */
}
</style>
  