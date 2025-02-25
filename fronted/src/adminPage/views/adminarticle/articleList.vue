<template>
  <!-- 搜索框 -->
  <div class="articlelist-header">
    <div class='section'>
      <label for="articleName">文章标题：</label>
      <input id="articleName" type="text" v-model="articleName" placeholder="请输入待查询文章标题"/>
    </div>
    <div class='section'>
      <label for="categoryList">文章分类：</label>
      <select v-model="category" id="categoryList">
        <option disabled value="">请选择</option>
        <option v-for="option in categoryList" :key="option" :value="option">{{ option }}</option>
      </select>
    </div>
    <div class='section'>
      <label for="articleStatus">文章状态：</label>
      <select v-model="Status" id="articleStatus">
        <option disabled value="">请选择</option>
        <option v-for="option in articleStatus" :key="option" :value="option">{{ option }}</option>
      </select>
    </div>
    <div class="section">
      <button class="search-btn" @click="searchOpition">搜索</button>
      <button class="reset-btn" @click="resetOption">重置</button>
    </div>
  </div>
  
  <!-- 基础操作 -->
  <div class="baseOption">
    <button class="addArticle-btn" @click="switchToArticlePost">添加文章</button>
    <button class="deleteArticle-btn" @click="() => deleteSelectedArticles()">删除文章</button>
  </div>

  <!-- 文章列表 -->
  <div class="table-container">
    <table>
      <!-- 表头 -->
      <thead>
        <tr>
          <th class="checkbox-column">
            <input type="checkbox" v-model="selectAll" @change="toggleSelectAll" />
          </th>
          <th class="id-column">编号</th>
          <th class="cover-column">封面</th>
          <th class="title-column">标题</th>
          <th class="summary-column">摘要</th>
          <th class="category-column">分类</th>
          <th class="status-column">状态</th>
          <th class="view-column">访问量</th>
          <th class="time-column">最后更新时间</th>
          <th class="action-column">操作</th>
        </tr>
      </thead>

      <!-- 表体 -->
      <tbody>
        <tr v-for="(article, index) in articles" :key="article.id">
          <td class="checkbox-column">
            <input type="checkbox" v-model="article.selected" />
          </td>
          <td class="id-column">{{ article.id }}</td>
          <td class="cover-column">
            <div class="cover-wrapper">
              <img v-if="article.imageSrc" :src="article.imageSrc" alt="封面" />
              <span v-else>暂无封面</span>
            </div>
          </td>
          <td class="title-column">{{ article.title }}</td>
          <td class="summary-column">{{ article.summary }}</td>
          <td class="category-column">{{ article.category }}</td>
          <td class="status-column">{{ article.status }}</td>
          <td class="view-column">{{ article.viewCount }}</td>
          <td class="time-column">{{ article.time }}</td>
          <td class="action-column">
            <button @click="editbaseArticle(article)" class="edit-base-option">基本</button>
            <button @click="editArticle(article)" class="edit-option">编辑</button>
            <button @click="deleteSelectedArticles([article.id])" class="delete-option">删除</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- 模态窗口 -->
  <changeModal v-model:visible="showModal" title="文章基础信息修改">
    <form @submit.prevent="saveChanges">
      <!-- ID -->
      <div class="form-item">
        <label for="id">ID:</label>
        <input id="id" type="text" v-model="currentArticle.id" disabled />
      </div>

      <div class="form-item">
        <label for="cover">封面:</label>
        <div class="background-section">
          <button class="change-background-btn" @click="fileInput.click()">修改背景</button>
          <input ref="fileInput" type="file" accept="image/*" @change="handleBackgroundChange" style="display: none;" />
        </div>
      </div>
      <!-- 图片预览 -->
      <div v-if="cover" class="preview-section">
        <p>背景预览：</p>
        <img :src="cover" alt="背景预览" class="background-preview" />
      </div>

      <!-- 标题 -->
      <div class="form-item">
        <label for="title">标题:</label>
        <input id="title" type="text" v-model="currentArticle.title" disabled />
      </div>

      <!-- 摘要 -->
      <div class="form-item">
        <label for="summary">摘要:</label>
        <textarea
          id="summary"
          v-model="currentArticle.summary"
          rows="4"
        ></textarea>
      </div>

      <!-- 分类 -->
      <div class="form-item">
        <label for="category">分类:</label>
        <select v-model="nowArticleCategory" id="allCategories">
          <option v-for="option in allCategories" :key="option" :value="option">{{ option }}</option>
        </select>
      </div>

      <!-- 状态 -->
      <div class="form-item">
        <label for="status">状态:</label>
        <select v-model="articlestatus" id="articleStatus">
          <option v-for="option in articleStatus" :key="option" :value="option">{{ option }}</option>
        </select>
      </div>

      <!-- 访问量 -->
      <div class="form-item">
        <label for="viewCount">访问量:</label>
        <input id="viewCount" type="number" v-model="currentArticle.viewCount" disabled />
      </div>

      <!-- 最后更新时间 -->
      <div class="form-item">
        <label for="time">最后更新时间:</label>
        <input id="time" type="text" v-model="currentArticle.time" disabled />
      </div>

      <!-- 保存按钮 -->
      <button type="submit" class="submit-edit-base-btn" @click="updateArticleBase">保存修改</button>
    </form>
  </changeModal>

  <!-- 分页控件 -->
  <div class="pagination">
    <button @click="goToPage(page - 1)" :disabled="page <= 1">上一页</button>
    <span>{{ page }} / {{ totalPages }}</span>
    <button @click="goToPage(page + 1)" :disabled="page >= totalPages">下一页</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { ElMessageBox, ElMessage } from 'element-plus';
import axios from "axios";
import CryptoJS from 'crypto-js';
import changeModal from "@/adminPage/components/changeModal.vue";

const emit = defineEmits(['updateView']);

const articleName = ref("");
const categoryList = ref([]);
const articleStatus = ['published', 'draft'];

const category = ref("");
const Status = ref("");

const page = ref(1); // 当前页数
const totalPages = ref(1); // 总页数
const articles = ref([]); // 初始为空数组
const currentArticle = ref({}); // 用于存储当前编辑的文章
const articlestatus = ref("")
const allCategories = ref([]);
const nowArticleCategory = ref("");
const cover = ref("");
const coverfile = ref(null);
const fileInput = ref(null); // 文件输入框的引用

const showModal = ref(false);

const fetchArticles = async () => {
  try {
    // 组装查询参数
    const params = {
      page: page.value, // 当前页数
    };
    if (category.value) {
      params.categoryName = category.value;
    }
    if (Status.value) {
      params.status = Status.value;
    }
    if (articleName.value) {
      params.title = articleName.value;
    }

    // 发起请求，带上查询参数
    const response = await axios.get("http://localhost:8001/api/admin/searchArticle/", {
      params, // Axios 会自动将对象转换为查询字符串
    });

    if (response.status === 200) {
      // 按后端返回的数据格式直接处理
      articles.value = response.data.results.map((article) => ({
        id: article.id,
        imageSrc: article.imageSrc || '', // 如果 imageSrc 为空，使用空字符串代替
        title: article.title,
        summary: article.summary || '暂无摘要', // 若 summary 为 null，则显示“暂无摘要”
        category: article.categoryName || '未分类', // 若 categoryName 为 null，则显示“未分类”
        status: article.status,
        viewCount: article.visits || 0, // 如果 visits 是 null 或 undefined，则默认为 0
        selected: false, // 前端状态
        time: article.updated_at, // 更新时间
      }));
      // 更新总页数
      totalPages.value = Math.ceil(response.data.count / 6);
    } else {
      console.error("后端数据格式不正确：", response.data);
    }
  } catch (error) {
    console.error("获取文章列表失败：", error);
  }
};

const fetchCategories = async () => {
  try {
    const response = await axios.get("http://localhost:8001/api/admin/categoryWithArticles/");
    if (response.status === 200 && Array.isArray(response.data)) {
      categoryList.value = response.data;
    } else {
      console.error("后端分类数据格式不正确：", response.data);
    }
  } catch (error) {
    console.error("获取分类列表失败：", error);
  }

  try {
    const response = await axios.get("http://localhost:8001/api/admin/categoriesoutsub/");
    if (response.status === 200 && Array.isArray(response.data)) {
      allCategories.value = response.data;
    } else {
      console.error("后端分类数据格式不正确：", response.data);
    }
  } catch (error) {
    console.error("获取分类列表失败：", error);
  }
};

onMounted(() => {
  fetchArticles(); // 组件挂载时调用获取数据的函数
  fetchCategories();
});

// 全选框的状态
const selectAll = ref(false);

// 切换全选/全不选
function toggleSelectAll() {
  articles.value.forEach(article => {
    article.selected = selectAll.value;
  });
}

// 分页跳转
function goToPage(newPage) {
  if (newPage >= 1 && newPage <= totalPages.value) {
    page.value = newPage;
    fetchArticles();
  }
}

// 搜索选项
function searchOpition() {
  page.value = 1;
  fetchArticles();
}

// 重置搜素选项
function resetOption() {
  articleName.value = "";
  category.value = "";
  Status.value = "";
}

// 添加文章函数
const switchToArticlePost = () => {
  // 通过 emit 发送事件，切换父组件的 currentView
  emit('updateView', 'articlePost');
};

const editArticle = (articleData) => {
  emit('updateView', 'articleEdit', articleData);
}

const getImageFile = async (imageSrc) => {
  if (!imageSrc) {
    return null;  // imageSrc 为 null 或 undefined 时返回 null
  }

  try {
    // 使用 fetch 从服务器加载图片
    const response = await fetch(imageSrc);
    if (response.ok) {
      // 转换为 Blob 类型
      const blob = await response.blob();
      
      // 提取 MIME 类型，确保使用正确的文件扩展名
      const contentType = blob.type; // MIME 类型，例如 "image/jpeg" 或 "image/png"
      const fileExtension = contentType.split('/')[1]; // 提取扩展名，例如 "jpeg" 或 "png"
      
      // 使用动态的文件扩展名
      const file = new File([blob], `image.${fileExtension}`, { type: contentType });
      
      return file;  // 返回文件对象
    } else {
      console.error("无法获取图片文件，响应不成功");
      return null;
    }
  } catch (error) {
    console.error("获取图片文件出错", error);
    return null;
  }
};

const editbaseArticle = async (articleData) => {
  currentArticle.value = { ...articleData };
  articlestatus.value = articleData.status;
  nowArticleCategory.value = articleData.category;
  cover.value = articleData.imageSrc;
  coverfile.value = await getImageFile(articleData.imageSrc);
  showModal.value = true;
}

// 删除选中文章
const deleteSelectedArticles = async (selectedArticles = null) => {
  // 获取选中文章的 id 数组
  if (!selectedArticles) {
    selectedArticles = articles.value.filter(article => article.selected).map(article => article.id);
  }

  if (selectedArticles.length === 0) {
    ElMessage.warning("请先选择要删除的文章！");
    return;
  }

  // 使用 ElMessageBox 弹出确认框
  ElMessageBox.confirm(
    '确定要删除这些文章吗？\n删除的文章无法找回。',
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  )
    .then(async () => {
      // 确认删除
      try {
        const response = await axios.post("http://localhost:8001/api/admin/deleteArticles/", {
          ids: selectedArticles
        });

        if (response.status === 200) {
          ElMessage.success("删除成功！");
          fetchArticles(); // 刷新当前页
        } else {
          ElMessage.error("删除失败！");
        }
      } catch (error) {
        console.error("删除文章失败：", error);
        ElMessage.error("删除失败！");
      }
    })
    .catch(() => {
      // 取消删除
      console.log("用户取消删除操作");
    });
};

function handleBackgroundChange(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = () => {
      cover.value = reader.result; // 更新背景图片
      coverfile.value = file;
    };
    reader.readAsDataURL(file);
  }
}

async function updateArticleBase() {
  // 图片处理
  let fileToServerName = null
  let imgId = null;
  try {
    const base64Image = cover.value.split(',')[1];
    const fileExtension = coverfile.value.name.split('.').pop();
    const hash = calculateSHA256(base64Image);
    const imgfileName = `${hash}.${fileExtension}`;
    const uploadPath = `.\\fronted\\public\\images\\`;
    // console.log(uploadPath);

    const uploadSuccess = uploadImageToServer(coverfile.value, imgfileName, uploadPath);
    if (!uploadSuccess) {
      alert('文件上传失败！');
      return;
    }
    fileToServerName = `.\\images\\${imgfileName}`;
  } catch (error) {
    // console.log("error!");
  }
  if (fileToServerName) {
    imgId = await uploadFileToServer(fileToServerName, coverfile.value.type, coverfile.value.size);
  }
  // console.log(imgId);
  await uploadArticleBase(imgId);

  // 刷新当前页面
  fetchArticles();

  showModal.value = false;
}

async function uploadArticleBase(bannar_id) {
  try {
    const formData = new FormData();
    formData.append('id', currentArticle.value.id);
    formData.append('bannar_id', bannar_id);
    formData.append('summary', currentArticle.value.summary);
    formData.append('categoryName', nowArticleCategory.value);
    formData.append('status', articlestatus.value);

    const response = await axios.post('http://localhost:8001/api/admin/updateArticleBase/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',  // 告诉服务器这次请求是上传文件
      },
    });

    if (response.status === 200) {
      // 上传成功，获取返回的 id
      console.log('文件上传成功');
    } else {
      console.log(response.status);
      console.error('文件上传失败:', response.data);
    }
  } catch (error) {
    console.error('修改文章基础信息出错:', error);
  }
}

async function uploadFileToServer(fileToServerName, fileType, fileSize) {
  let uploadedFileId = null;  // 用于存储上传成功后的文件ID

  // console.log(fileToServerName);
  // console.log(fileType);
  // console.log(fileSize);

  try {
    // 创建 FormData 对象来处理文件上传
    const formData = new FormData();
    
    // 将文件路径、文件类型和文件大小添加到 FormData
    formData.append('file', fileToServerName);
    formData.append('fileType', fileType);
    formData.append('fileSize', fileSize);

    // 发送 POST 请求到后端接口
    const response = await axios.post('http://localhost:8001/api/admin/addMedia/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',  // 告诉服务器这次请求是上传文件
      },
    });

    if (response.status === 201 || response.status === 200) {
      // 上传成功，获取返回的 id
      uploadedFileId = response.data.id;
      console.log('文件上传成功, 返回的 ID:', uploadedFileId);
    } else {
      console.log(response.status);
      console.error('文件上传失败:', response.data);
    }
  } catch (error) {
    console.error('上传文件时出错:', error);
  }

  // 返回上传的文件 ID（如果失败则为 null）
  return uploadedFileId;
}

const calculateSHA256 = (data) => {
  const hash = CryptoJS.SHA256(data);  // 使用 crypto-js 计算 SHA-256
  return hash.toString(CryptoJS.enc.Hex);  // 转换为十六进制字符串
};

const uploadImageToServer = async (file, fileName, address) => {
  const formData = new FormData();
  formData.append('file', file, fileName);
  formData.append('address', address);

  // 打印 FormData 内容
  // for (let pair of formData.entries()) {
  //   console.log(pair[0] + ': ' + pair[1]);
  // }

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
.articlelist-header {
  padding-right: 20%;
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: center;
  justify-content: space-between;
}

.section {
  display: flex;
  flex-direction: row;
  gap: 10px;
}

.section label {
  display: flex;
  align-items: center;
  font-size: 1.2em;
}

.section input,
.section select {
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-sizing: border-box;
}

.section input:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.search-btn, .reset-btn {
  padding: 5px 12px;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
}

.search-btn {
  background-color: #007bff;
  color: white;
  border: none;
}

.search-btn:hover {
  background-color: #0056b3;
}

.reset-btn {
  color: grey;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
}

.reset-btn:hover {
  background-color: #e0e0e0;
}

.baseOption {
  margin-top: 1em;
  display: flex;
  flex-direction: row;
  gap: 1em;
}

.addArticle-btn, .deleteArticle-btn {
  padding: 5px 12px;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
}

.addArticle-btn {
  background-color: #007bff;
  color: white;
  border: none;
}

.addArticle-btn:hover {
  background-color: #0056b3;
}

.deleteArticle-btn {
  color: grey;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
}

.deleteArticle-btn:hover {
  background-color: #e0e0e0;
}

.table-container {
  margin: 20px;
  margin-left: 0;
  overflow-x: auto; /* 表格宽度溢出时可滚动 */
}

table {
  width: 85%; /* 固定表格宽度 */
  border-collapse: collapse; /* 合并边框 */
  text-align: left;
  table-layout: fixed; /* 固定列宽 */
}

th, td {
  padding: 10px;
  border-bottom: 1px solid #e0e0e0;
  overflow: hidden;
  text-overflow: ellipsis; /* 超出宽度时显示省略号 */
  white-space: nowrap; /* 防止换行 */
}

th {
  background-color: #f4f4f4;
  font-weight: bold;
  text-align: center;
}

.checkbox-column {
  width: 40px;
  text-align: center;
}

.id-column {
  width: 50px;
}

.cover-column {
  width: 100px;
}

.title-column {
  width: 150px;
}

.summary-column {
  width: 180px;
}

.category-column {
  width: 100px;
}

.status-column {
  width: 100px;
}

.view-column {
  width: 80px;
}

.time-column {
  width: 160px;
}

.action-column {
  width: 120px;
  text-align: center;
}

.cover-wrapper {
  width: 100px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  overflow: hidden;
}

.cover-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 图片填充容器 */
}

.cover-wrapper span {
  font-size: 12px;
  color: #aaa;
}

.edit-option, .delete-option, .edit-base-option {
  background: none;
  border: none;
  font-size: 0.8em;
  color: grey;
  cursor: pointer; 
  transition: background-color 0.3s; 
}

.edit-option:hover, .delete-option:hover, .edit-base-option:hover {
  color: #003687;
}

.submit-edit-base-btn {
  /* width: 100%; */
  padding: 5px 12px;
  font-size: 0.85em;
  border-radius: 4px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}

.pagination button {
  padding: 5px 15px;
  font-size: 14px;
  cursor: pointer;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination span {
  padding: 5px 10px;
  font-size: 16px;
}
</style>
