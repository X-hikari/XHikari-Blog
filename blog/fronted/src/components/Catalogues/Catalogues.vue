<template>
  <div class="catalogues">
    <div class="sticky-header">
        <div class="Cataloguestitle" @click="handle()">文章目录</div>
        <ul>
        <li v-for="(catalogue, index) in directories" :key="index">
          <span :class="{'active': shouldcolor(catalogue.id)}" @click="parent()">{{ catalogue.name }}</span>
          <!-- 判断是否展开子目录 -->
          <CatalogueItem 
            v-if="catalogue.children && catalogue.children.length && shouldExpand(catalogue.id)" 
            :directories="catalogue.children" 
            :activeRoot="activeRoot"
          />
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useParentIdStore } from '@/stores/parentID';
import CatalogueItem from '@/components/Catalogues/CatalogueItem.vue';

// 定义组件的 prop
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

const handle= () => {
  alert(props.activeRoot);
}

const parent= () => {
  console.log(parentIdStore.parentId);
}

// 使用 Pinia Store
const parentIdStore = useParentIdStore();

// 判断当前目录是否应该展开
const shouldExpand = (catalogueId) => {
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

span {
  font-weight: bold;
}

.active {
  color: rgba(145, 196, 238); /* 当前项的字体颜色为蓝色 */
}
</style>
  