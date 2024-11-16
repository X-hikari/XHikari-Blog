import { defineStore } from 'pinia';

export const useParentIdStore = defineStore('parentId', {
  // 定义状态
  state: () => ({
    activeRoot: null,
    parentId: [], // 用于存储当前激活目录的所有父节点 ID
    children: [],
  }),

  // 定义 actions
  actions: {
    // 更新父节点
    setParentId(catalogueId, directories) {
      // 找到当前目录
      const catalogue = directories.find((item) => item.id === catalogueId);
      if (catalogue) {
        this.activeRoot = catalogue.id;
        this.parentId = catalogue.parent; // 假设每个目录的 `parent` 是一个包含父目录的数组
        this.children = catalogue.children.map(child => child.id);
      }
    },
    // 判断当前目录是否是祖先
    isAncestor(catalogueId) {
      return this.parentId.includes(catalogueId);
    },
  },

});
