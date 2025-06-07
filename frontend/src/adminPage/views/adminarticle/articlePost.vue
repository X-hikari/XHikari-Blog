<template>
  <div class="admin-app">
    <!-- Markdown 编辑器 -->
    <md-editor ref="editorRef" v-model="editorValue" height="400px" class="editor" @paste="handlePaste" />
    <div class="operation">
      <el-button type="primary" @click="triggerArticleUpload('draft')" v-if="mode === 'create'">保存</el-button>
      <el-button type="primary" @click="triggerArticleUpload('published')" v-if="mode === 'create'">发布</el-button>
      <el-button type="primary" @click="triggerArticleUpdate()" v-if="mode === 'edit'">保存</el-button>
      <el-button type="default" @click="resetArticle" v-if="mode === 'edit'">重置</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';
import { MdEditor } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css'; // 引入样式
import CryptoJS from 'crypto-js';
import { ElButton } from 'element-plus';
import 'element-plus/dist/index.css';  // 引入 Element Plus 样式

// Markdown 内容
const editorValue = ref('# 这是一个 Markdown 编辑器');
const editorRef = ref(null);  // 用来获取 MdEditor 实例

// 当前模式，'create'表示发布文章，'edit'表示修改文章
const props = defineProps({
  mode: {
    type: String,
    required: true
  }, 
  articleData: {
    type: Object,
    default: () => ({})  // 默认值为空对象
  }
});

const fetchArticleContent = async (id) => {
  try {
    const response = await axios.get(`http://localhost:8001/api/admin/articleContent/`, {
      params: { id }
    });
    if (response.status === 200) {
      // 如果获取成功，将内容加载到编辑器中
      editorValue.value = response.data.content || '';
    }
  } catch (error) {
    console.error('获取文章内容失败', error);
    editorValue.value = '';  // 如果获取失败，清空编辑器内容
  }
};

// 监听 mode 和 articleData 的变化
watch(() => props.mode, (newMode) => {
  if (newMode === 'edit' && props.articleData.id) {
    // 调用 API 获取文章内容
    fetchArticleContent(props.articleData.id);
  }
  if (newMode === 'create') {
    editorValue.value = "# 这是一个 Markdown 编辑器";
  }
}, { immediate: true });   // immediate: true 使得在组件加载时就立即执行

const resetArticle = () => {
  fetchArticleContent(props.articleData.id);  // 清空或加载原始内容
};

const triggerArticleUpload = (status) => {
  // 获取编辑器中的 Markdown 内容
  const content = editorValue.value;

  // 使用正则表达式提取第一个 # 开头的行作为标题
  const titleMatch = content.match(/^# (.+)$/m);  // 以 # 开头的行

  let title = 'Untitled';

  if (titleMatch && titleMatch[1]) {
    title = titleMatch[1].trim();  // 提取标题并去除多余的空格
  }

  // console.log('文章标题:', title);
  // console.log('文章内容:', content);
  // console.log('文章状态:', status);

  const articleData = {
    title,
    content,
    status
  };

  uploadArticle(articleData);
}

const triggerArticleUpdate = () => {
  // 获取编辑器中的 Markdown 内容
  const content = editorValue.value;

  // 使用正则表达式提取第一个 # 开头的行作为标题
  const titleMatch = content.match(/^# (.+)$/m);  // 以 # 开头的行

  let title = 'Untitled';

  if (titleMatch && titleMatch[1]) {
    title = titleMatch[1].trim();  // 提取标题并去除多余的空格
  }

  const articleData = {
    id:props.articleData.id,
    title,
    content,
  };

  updateArticle(articleData, 'http://localhost:8001/api/admin/updateArticleContent/');
}

const updateArticle = async (articleData, web) => {
  try {
    const response = await axios.post(web, articleData, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',  // 告诉服务器返回 JSON 格式
      },
    });
    if (response.status === 200) {
      alert("修改成功");
      return true;
    } else {
      alert("修改失败");
      console.error('修改失败', response.data);
      return false;
    }
  } catch (error) {
    alert("修改出错");
    console.error('修改出错', error);
    return false;
  }
}

const uploadArticle = async (articleData) => {
  // console.log(articleData);
  try {
    const response = await axios.post('http://localhost:8001/api/admin/addArticle/', articleData, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',  // 告诉服务器返回 JSON 格式
      },
    });
    if (response.status === 200) {
      alert("上传成功");
      return true;
    } else {
      alert("上传失败");
      console.error('上传失败', response.data);
      return false;
    }
  } catch (error) {
    alert("上传出错");
    console.error('上传出错', error);
    return false;
  }
}

// 处理粘贴事件
const handlePaste = (event) => {
  const items = event.clipboardData.items;
  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    if (item.type.indexOf('image') !== -1) {
      const file = item.getAsFile();
      if (file) {
        handleImage(file);
      }
    }
  }
};

const handleImage = async (file) => {
  const reader = new FileReader();

  // Step 1: 读取文件内容
  reader.onloadend = async () => {
    const base64Image = reader.result.split(',')[1]; // 获取 Base64 数据，不包括前缀
    const fileExtension = file.name.split('.').pop(); // 提取文件后缀

    // Step 2: 计算 SHA-256 哈希值
    const hash = calculateSHA256(base64Image);

    // Step 3: 生成文件名
    const fileName = `${hash}.${fileExtension}`;
    const uploadPath = `/uploads/${fileName}`;

    // Step 4: 上传文件到服务器
    const uploadSuccess = await uploadImageToServer(file, fileName);
    if (!uploadSuccess) {
      alert('文件上传失败！');
      return;
    }

    // Step 5: 构造 Markdown 图片语法
    const markdownImage = `![图片正在加载](${uploadPath})`;

    // Step 6: 插入图片到当前光标位置
    insertAtCursorInEditor(markdownImage);
  };

  reader.readAsDataURL(file);
};

const insertAtCursorInEditor = (content) => {
  // console.log(content);
  editorRef.value?.insert(() => {
    // console.log(content);
    return {
      /**
     * @return targetValue    待插入内容
     * @return select         插入后是否自动选中内容，默认：true
     * @return deviationStart 插入后选中内容鼠标开始位置，默认：0
     * @return deviationEnd   插入后选中内容鼠标结束位置，默认：0
     */
      targetValue: `${content}`,
      select: false,
      deviationStart: 0,
      deviationEnd: 0,
    };
  });
};

// 工具函数：计算 SHA-256 哈希
const calculateSHA256 = (data) => {
  const hash = CryptoJS.SHA256(data);  // 使用 crypto-js 计算 SHA-256
  return hash.toString(CryptoJS.enc.Hex);  // 转换为十六进制字符串
};

// 工具函数：上传图片到服务器
const uploadImageToServer = async (file, fileName) => {
  const formData = new FormData();
  formData.append('file', file, fileName);

  try {
    const response = await axios.post('http://localhost:8001/api/admin/upload/', formData, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',  // 告诉服务器返回 JSON 格式
      },
    });
    if (response.status === 200) {
      return true;
    } else {
      console.error('上传失败', response.data);
      return false;
    }
  } catch (error) {
    console.error('上传出错', error);
    return false;
  }
};

</script>

<style scoped>
.admin-app {
  font-family: Arial, sans-serif;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
  /* width: 100vw; */
  box-sizing: border-box;
}

.editor-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
  width: 100%;
}

.editor {
  width: 100%;
  max-width: 1000px;
  box-sizing: border-box;
  margin-bottom: 20px;
}

.preview {
  margin-top: 20px;
  padding: 20px;
  width: 100%;
  max-width: 1000px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #ddd;
}
</style>
