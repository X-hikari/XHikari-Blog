<template>
  <ul>
    <li v-for="(catalogue, index) in directories" :key="index">
      <span :class="{'active': shouldcolor(catalogue.id)}">{{ catalogue.name }}</span>

      <!-- 判断是否展开当前目录的子目录 -->
      <CatalogueItem 
        v-if="shouldExpand(catalogue.id)" 
        :directories="catalogue.children" 
        :activeRoot="activeRoot"
        :parentId="parentId"      
      />
    </li>
  </ul>
</template>

<script setup>
import { ref } from 'vue';
import CatalogueItem from '@/components/Catalogues/CatalogueItem.vue';

const props = defineProps({
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

<style scoped>
ul {
  padding-left: 15px;
  list-style-type: none;
}

li {
  margin: 2px 0;
}

.active {
  color: rgba(145, 196, 238); /* 当前项的字体颜色为蓝色 */
}
</style>
