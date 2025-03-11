<template>
  <ul>
    <li v-for="(catalogue, index) in directories" :key="index">
      <span :class="['Text', {'active': shouldcolor(catalogue.id)}]" @click="jumpRoot(catalogue.id)">{{ catalogue.name }}</span>

      <!-- 判断是否展开当前目录的子目录 -->
      <CatalogueItem 
        v-if="shouldExpand(catalogue.id)" 
        :directories="catalogue.children" 
        :activeRoot="activeRoot"
        :parentId="parentId"
        @update-jump-root="updateToParent"      
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

const emit = defineEmits(['update-jump-root']);
const jumpRoot = (catalogueId) => {
  emit('update-jump-root', catalogueId);
};

const updateToParent = (catalogueId) => {
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

<style scoped>
ul {
  padding-left: 15px;
  list-style-type: none;
}

li {
  margin: 2px 0;
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
