<template>
  <div class="categorylist-header">
    <div class="section">
      <label for="parentCategory">父分类</label>
      <select id="parentCategory" type="text" v-model="parentCategory">
        <option disabled value="">请选择</option>
        <option v-for="option in parentCategoryList" :key="option" :value="option">{{ option }}</option>
      </select>
    </div>
    <div class="section">
      <button class="search-btn" @click="searchOpition">搜索</button>
      <button class="reset-btn" @click="resetOption">重置</button>
    </div>
  </div>

  <!-- 基础操作 -->
  <div class="baseOption">
    <button class="addCategory-btn" @click="addCategory">添加分类</button>
    <button class="deleteCategory-btn" @click="() => deleteSelectedCategories()">删除分类</button>
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
          <th class="name-colunm">类名</th>
          <th class="description-column">简介</th>
          <th class="number-column">文章数目</th>
          <th class="parent-column">父类</th>
          <th class="time-column">最后更新时间</th>
          <th class="action-column">操作</th>
        </tr>
      </thead>

      <!-- 表体 -->
      <tbody>
        <tr v-for="(category, index) in categories" :key="category.id">
          <td class="checkbox-column">
            <input type="checkbox" v-model="category.selected" />
          </td>
          <td class="id-column">{{ category.id }}</td>
          <td class="cover-column">
            <div class="cover-wrapper">
              <img v-if="category.imageSrc" :src="category.imageSrc" alt="封面" />
              <span v-else>暂无封面</span>
            </div>
          </td>
          <td class="name-colunm">{{ category.name }}</td>
          <td class="description-column">{{ category.description }}</td>
          <td class="number-column">{{ category.number }}</td>
          <td class="parent-column">{{ category.parent }}</td>
          <td class="time-column">{{ category.time }}</td>
          <td class="action-column">
            <button @click="editCategory(category)" class="edit-option">修改</button>
            <button @click="deleteSelectedCategories([category.id])" class="delete-option">删除</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- 分页控件 -->
  <div class="pagination">
    <button @click="goToPage(page - 1)" :disabled="page <= 1">上一页</button>
    <span>{{ page }} / {{ totalPages }}</span>
    <button @click="goToPage(page + 1)" :disabled="page >= totalPages">下一页</button>
  </div>

  <!-- 模态窗口-添加分类 -->
  <changeModal v-model:visible="showModalAdd" title="分类添加窗口">
    <form @submit.prevent="saveChanges">
      
      <!-- 封面 -->
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

      <!-- 类名 -->
      <div class="form-item">
        <label for="name">类名:</label>
        <input id="name" type="text" v-model="addName" />
      </div>

      <!-- 介绍 -->
      <div class="form-item">
        <label for="description">介绍:</label>
        <textarea
          id="description"
          v-model="addDescription"
          rows="4"
        ></textarea>
      </div>

      <!-- 父类 -->
      <div class="form-item">
        <label for="parent">父类:</label>
        <select v-model="addParent" id="allCategories">
          <option value="">无</option>
          <option v-for="option in parentCategoryList" :key="option" :value="option">{{ option }}</option>
        </select>
      </div>

      <!-- 保存按钮 -->
      <button type="submit" class="submit-edit-base-btn" @click="update_add_CategoryBase('add')">添加分类</button>
    </form>
  </changeModal>

  <!-- 模态窗口-修改分类 -->
  <changeModal v-model:visible="showModalEdit" title="分类添加窗口">
    <form @submit.prevent="saveChanges">
      <!-- ID -->
      <div class="form-item">
        <label for="id">ID:</label>
        <input id="id" type="text" v-model="currentCategory.id" disabled />
      </div>

      <!-- 封面 -->
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

      <!-- 类名 -->
      <div class="form-item">
        <label for="name">类名:</label>
        <input id="name" type="text" v-model="currentCategory.name" />
      </div>

      <!-- 介绍 -->
      <div class="form-item">
        <label for="description">介绍:</label>
        <textarea
          id="description"
          v-model="currentCategory.description"
          rows="4"
        ></textarea>
      </div>

      <!-- 文章数目 -->
      <div class="form-item">
        <label for="number">文章数目:</label>
        <input id="number" type="text" v-model="currentCategory.number" disabled />
      </div>

      <!-- 父类 -->
      <div class="form-item">
        <label for="parent">父类:</label>
        <select v-model="editParent" id="allCategories">
          <option value="">无</option>
          <option v-for="option in parentCategoryList" :key="option" :value="option">{{ option }}</option>
        </select>
      </div>

      <!-- 保存按钮 -->
      <button type="submit" class="submit-edit-base-btn" @click="update_add_CategoryBase('edit')">保存修改</button>
    </form>
  </changeModal>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { ElMessageBox, ElMessage } from 'element-plus';
import axios from "axios";
import CryptoJS from 'crypto-js';
import changeModal from "@/adminPage/components/changeModal.vue";

const showModalAdd = ref(false);
const showModalEdit = ref(false);

const page = ref(1); // 当前页数
const totalPages = ref(1); // 总页数

const parentCategoryList = ref([]);
const parentCategory = ref("");
const categories = ref([]); // 初始为空数组

const cover = ref("");
const coverfile = ref(null);
const fileInput = ref(null); // 文件输入框的引用

const addName = ref("");
const addDescription = ref("");
const addParent = ref("");

const currentCategory = ref({})
const editParent = ref("")

const editCategory = async (categoryData) => {
  currentCategory.value = { ...categoryData };
  editParent.value = categoryData.parent;
  cover.value = categoryData.imageSrc;
  coverfile.value = await getImageFile(categoryData.imageSrc);
  showModalEdit.value = true;
}

const addCategory = async () => {
  cover.value = null;
  coverfile.value = null;
  showModalAdd.value = true;
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

const fetchAllCategoriesName = async () => {
  try {
    const response = await axios.get("http://localhost:8001/api/admin/categoryName/");
    
    if (response.status === 200) {
      parentCategoryList.value = response.data;
    }
  } catch (error) {
    console.error("获取分类名称失败：", error);
  }
};

const fetchCategories = async () => {
  try {
    // 组装查询参数
    const params = {
      page: page.value, // 当前页数
    };
    if (parentCategory.value) {
      params.parent = parentCategory.value;
    }

    // 发起请求，带上查询参数
    const response = await axios.get("http://localhost:8001/api/admin/serachCategory/", {
      params, // Axios 会自动将对象转换为查询字符串
    });

    if (response.status === 200) {
      // 按后端返回的数据格式直接处理
      categories.value = response.data.results.map((category) => ({
        id: category.id,
        imageSrc: category.imageSrc || '', // 如果 imageSrc 为空，使用空字符串代替
        name: category.name,
        description: category.description || '暂无描述', // 若 summary 为 null，则显示“暂无摘要”
        number: category.article_count || 0,
        parent: category.parent || '无父类', // 若 categoryName 为 null，则显示“未分类”
        selected: false, // 前端状态
        time: category.updated_at, // 更新时间
      }));
      // 更新总页数
      totalPages.value = Math.ceil(response.data.count / 6);
    } else {
      console.error("后端数据格式不正确：", response.data);
    }
  } catch (error) {
    console.error("获取分类列表失败：", error);
  }
};

onMounted(() => {
  fetchCategories(); // 组件挂载时调用获取数据的函数
  fetchAllCategoriesName();
});

// 全选框的状态
const selectAll = ref(false);

// 切换全选/全不选
function toggleSelectAll() {
  categories.value.forEach(category => {
    category.selected = selectAll.value;
  });
}

// 分页跳转
function goToPage(newPage) {
  if (newPage >= 1 && newPage <= totalPages.value) {
    page.value = newPage;
    fetchCategories();
  }
}

// 搜索选项
function searchOpition() {
  page.value = 1;
  fetchCategories();
}

// 重置搜素选项
function resetOption() {
  parentCategory.value = "";
}

function handleBackgroundChange(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = () => {
      cover.value = reader.result;
      coverfile.value = file;
    };
    reader.readAsDataURL(file);
  }
}

async function update_add_CategoryBase(method) {
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
  if (method === 'add') {
    await addNewCategory(imgId);
  } else if (method === 'edit') {
    await updateNewCategory(imgId);
  }

  // 刷新当前页面
  fetchCategories();

  showModalAdd.value = false;
  showModalEdit.value = false;
}

async function updateNewCategory(bannar_id) {
  try {
    const formData = new FormData();
    formData.append('id', currentCategory.value.id);
    formData.append('name', currentCategory.value.name);
    formData.append('bannar_id', bannar_id);
    formData.append('description', currentCategory.value.description);
    formData.append('parent', currentCategory.value.parent);

    const response = await axios.post('http://localhost:8001/api/admin/updateCategory/', formData, {
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
    console.error('添加分类出错:', error);
  }
}

async function addNewCategory(bannar_id) {
  try {
    const formData = new FormData();
    formData.append('name', addName.value);
    formData.append('bannar_id', bannar_id);
    formData.append('description', addDescription.value);
    formData.append('parent', addParent.value);

    const response = await axios.post('http://localhost:8001/api/admin/addCategory/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',  // 告诉服务器这次请求是上传文件
      },
    });

    if (response.status === 201) {
      // 上传成功，获取返回的 id
      console.log('文件上传成功');
    } else {
      console.log(response.status);
      console.error('文件上传失败:', response.data);
    }
  } catch (error) {
    console.error('添加分类出错:', error);
  }
}

async function uploadFileToServer(fileToServerName, fileType, fileSize) {
  let uploadedFileId = null;  // 用于存储上传成功后的文件ID

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

// 删除选中分类
const deleteSelectedCategories = async (selectedCategories = null) => {
  // 获取选中分类的 id 数组
  console.log("selectedCategories ", selectedCategories);
  if (!selectedCategories) {
    selectedCategories = categories.value.filter(category => category.selected).map(category => category.id);
  }

  if (selectedCategories.length === 0) {
    ElMessage.warning("请先选择要删除的分类！");
    return;
  }

  // 使用 ElMessageBox 弹出确认框
  ElMessageBox.confirm(
    '确定要删除这些分类吗？删除的分类无法找回。\n该分类下的所有分类和文章都会一并被删除。',
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
        const response = await axios.post("http://localhost:8001/api/admin/deleteCategories/", {
          ids: selectedCategories
        });

        if (response.status === 200) {
          ElMessage.success("删除成功！");
          fetchCategories(); // 刷新当前页
        } else {
          ElMessage.error("删除失败！");
        }
      } catch (error) {
        console.error("删除分类失败：", error);
        ElMessage.error("删除失败！");
      }
    })
    .catch(() => {
      // 取消删除
      console.log("用户取消删除操作");
    });
};
</script>

<style>
.categorylist-header {
  padding-right: 20%;
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  gap: 60px;
  align-items: center;
  /* justify-content: space-between; */
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

.addCategory-btn, .deleteCategory-btn {
  padding: 5px 12px;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
}

.addCategory-btn {
  background-color: #007bff;
  color: white;
  border: none;
}

.addCategory-btn:hover {
  background-color: #0056b3;
}

.deleteCategory-btn {
  color: grey;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
}

.deleteCategory-btn:hover {
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

.name-colunm {
  width: 120px;
}

.description-column {
  width: 240px;
}

.number-column {
  width: 80px;
}

.parent-column {
  width: 120px;
}

.time-column {
  width: 160px;
}

.action-column {
  width: 80px;
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

.edit-option, .delete-option {
  background: none;
  border: none;
  font-size: 0.8em;
  color: grey;
  cursor: pointer; 
  transition: background-color 0.3s; 
}

.edit-option:hover, .delete-option:hover {
  color: #003687;
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
</style>