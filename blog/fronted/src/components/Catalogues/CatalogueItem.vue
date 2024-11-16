<template>
  <ul>
    <li v-for="(catalogue, index) in directories" :key="index">
      <span :class="{'active': shouldcolor(catalogue.id)}">{{ catalogue.name }}</span>

      <!-- 判断是否展开当前目录的子目录 -->
      <CatalogueItem 
        v-if="shouldExpand(catalogue.id)" 
        :directories="catalogue.children" 
        :activeRoot="activeRoot" 
      />
    </li>
  </ul>
</template>

<script setup>
import { ref } from 'vue';
import { useParentIdStore } from '@/stores/parentID';
import CatalogueItem from '@/components/Catalogues/CatalogueItem.vue';

const props = defineProps({
  directories: {
    type: Array,
    required: true
  },
  activeRoot: {
    type: Number, // 根目录 ID
    required: false
  }
});

// 使用 Pinia Store
const parentIdStore = useParentIdStore();

// 判断当前目录是否应该展开
const shouldExpand = (catalogueId) => {
  // console.log(catalogueId, props.activeRoot);
  if (props.activeRoot === catalogueId) {
    if (props.activeRoot !== parentIdStore.activeRoot) {
      parentIdStore.setParentId(catalogueId, props.directories);
    }
    return true;
  }
  if (parentIdStore.children.includes(props.activeRoot)) {
    return true;
  }
  // 检查当前目录是否是激活目录的祖先
  return parentIdStore.isAncestor(catalogueId)
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
