<template>
  <div class="media-header">
    <div class="section">
      <label for="limits">说说权限：</label>
      <select v-model="limit" id="limits">
        <option disabled value="">请选择</option>
        <option v-for="option in limits" :key="option" :value="option">{{ option }}</option>
      </select>

      <div class="section">
        <button class="search-btn" @click="searchOpition">搜索</button>
        <button class="reset-btn" @click="resetOption">重置</button>
      </div>
    </div>

    <div class="baseOption">
      <button class="addemotion-btn" @click="addEmotion">发表说说</button>
      <button class="deleteemotion-btn" @click="() => deleteSelectedEmotions()">删除说说</button>
    </div>
  </div>

  <!-- 说说列表 -->
  <div class="table-container">
    <table>
      <!-- 表头 -->
      <thead>
        <tr>
          <th class="checkbox-column">
            <input type="checkbox" v-model="selectAll" @change="toggleSelectAll" />
          </th>
          <th class="id-column">编号</th>
          <th class="content-column">说说内容</th>
          <th class="time-column">发表时间</th>
          <th class="limit-column">说说权限</th>
          <th class="action-column">操作</th>
        </tr>
      </thead>

      <!-- 表体 -->
      <tbody>
        <tr v-for="(emotion, index) in emotions" :key="emotion.id">
          <td class="checkbox-column">
            <input type="checkbox" v-model="emotion.selected" />
          </td>
          <td class="id-column">{{ emotion.id }}</td>
          <td class="content-column">{{ emotion.content }}</td>
          <td class="time-column">{{ emotion.time }}</td>
          <td class="limit-column">{{ emotion.limit }}</td>
          <td class="action-column">
            <button @click="editEmotion(emotion)" class="edit-option">编辑</button>
            <button @click="deleteSelectedEmotions([emotion.id])" class="delete-option">删除</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <changeModal v-model:visible="showModalAdd" title="发表说说">
    <div class="form-item">
      <label for="">说说权限:</label>
      <select v-model="addLimit" id="limit">
        <option v-for="option in limits" :key="option" :value="option">{{ option }}</option>
      </select>
    </div>

    <div class="form-item">
      <label for="content">内容:</label>
      <textarea id="content" v-model="addContent" rows="4"></textarea>
    </div>

    <div class="form-item">
      <label for="cover">图片:</label>
      <div class="background-section">
        <button class="change-background-btn" @click="triggerFileInput">添加图片</button>
        <input ref="fileInput" type="file" multiple accept="image/*" @change="handleFileUpload" style="display: none;" />
      </div>
    </div>

    <!-- 图片预览区域 -->
    <div class="image-preview">
      <div v-for="(image, index) in previewImages" :key="index" class="image-container">
        <img :src="image.url" class="preview-img" />
        <button class="remove-btn" @click="removeImage(index, 'add')">✖</button>
      </div>
    </div>

    <button class="submit-edit-base-btn" @click="submitEmotion">发表</button>
  </changeModal>

  <!-- 修改说说 -->
  <changeModal v-model:visible="showModalEdit" title="修改说说">
    <div class="form-item">
      <label for="id">编号</label>
      <input id="id" type="text" v-model="currentEmotion.id" disabled />
    </div>
    
    <div class="form-item">
      <label for="time">发表时间</label>
      <input id="time" type="text" v-model="currentEmotion.time" disabled />
    </div>

    <div class="form-item">
      <label for="limit">说说权限:</label>
      <select v-model="currentEmotion.limit" id="limit">
        <option v-for="option in limits" :key="option" :value="option">{{ option }}</option>
      </select>
    </div>

    <div class="form-item">
      <label for="content">内容:</label>
      <textarea id="content" v-model="currentEmotion.content" rows="4"></textarea>
    </div>

    <div class="form-item">
      <label for="cover">图片:</label>
      <div class="background-section">
        <button class="change-background-btn" @click="triggerFileInput">添加图片</button>
        <input ref="fileInput" type="file" multiple accept="image/*" @change="handleFileUpdate" style="display: none;" />
      </div>
    </div>

    <!-- 图片预览区域 -->
    <div class="image-preview">
      <div v-for="(image, index) in editImages" :key="index" class="image-container">
        <img :src="getImageSrc(image)" class="preview-img" />
        <button class="remove-btn" @click="removeImage(index, 'edit')">✖</button>
      </div>
    </div>

    <button class="submit-edit-base-btn" @click="updateEmotion">修改</button>
  </changeModal>

  <!-- 分页控件 -->
  <div class="pagination">
    <button @click="goToPage(page - 1)" :disabled="page <= 1">上一页</button>
    <span>{{ page }} / {{ totalPages }}</span>
    <button @click="goToPage(page + 1)" :disabled="page >= totalPages">下一页</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessageBox, ElMessage, imageEmits } from 'element-plus';
import axios from "axios";
import changeModal from '@/adminPage/components/changeModal.vue';

const limit = ref("");
const limits = ref(["公开", "私密"]);
const currentEmotion = ref({});

const emotions = ref([]);

const showModalAdd = ref(false);
const showModalEdit = ref(false);

const addContent = ref("");
const addLimit = ref('公开');
const previewImages = ref([]);
const editImages = ref([]);
const fileInput = ref(null);

const page = ref(1);
const totalPages = ref(1);

const selectAll = ref(false);

onMounted(() => {
  fetchEmotions();
});

// 搜索选项
function searchOpition() {
  page.value = 1;
  fetchEmotions();
}

// 重置搜素选项
function resetOption() {
  limits.value = "";
}

// 切换全选/全不选
function toggleSelectAll() {
  emotions.value.forEach(emotion => {
    emotion.selected = selectAll.value;
  });
}

const fetchEmotions = async () => {
  const params = {
    page: page.value, // 当前页数
  };
  if (limit) {
    params.limit = limit.value;
  }

  try {
    const response = await axios.get("http://localhost:8001/api/admin/searchEmotion/", {
      params,
    });

    if (response.status === 200) {
      emotions.value = response.data.results.map((emotion) => ({
        id: emotion.id,
        content: emotion.content,
        time: emotion.created_at,
        limit: emotion.status
      }));
    } else {
      console.error("后端说说数据格式不正确：", response.data);
    }
  } catch (error) {
    console.error("获取说说列表失败：", error);
  }
}

const addEmotion = async () => {
  showModalAdd.value = true;
}

// 删除选中说说
const deleteSelectedEmotions = async (selectedEmotions = null) => {
  // 获取选中说说的 id 数组
  if (!selectedEmotions) {
    selectedEmotions = emotions.value.filter(emotion => emotion.selected).map(emotion => emotion.id);
  }

  if (selectedEmotions.length === 0) {
    ElMessage.warning("请先选择要删除的说说！");
    return;
  }

  // 使用 ElMessageBox 弹出确认框
  ElMessageBox.confirm(
    '确定要删除这些说说吗？\n删除的说说无法找回。',
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
        const response = await axios.post("http://localhost:8001/api/admin/deleteEmotions/", {
          ids: selectedEmotions
        });

        if (response.status === 200) {
          ElMessage.success("删除成功！");
          fetchEmotions(); // 刷新当前页
        } else {
          ElMessage.error("删除失败！");
        }
      } catch (error) {
        console.error("删除说说失败：", error);
        ElMessage.error("删除失败！");
      }
    })
    .catch(() => {
      // 取消删除
      console.log("用户取消删除操作");
    });
};

// 触发文件选择
const triggerFileInput = () => {
  fileInput.value.click();
};

// 处理图片上传预览
const handleFileUpload = (event) => {
  const files = event.target.files;
  if (files.length) {
    Array.from(files).forEach(file => {
      const reader = new FileReader();
      reader.onload = (e) => {
        previewImages.value.push({ file, url: e.target.result });
      };
      reader.readAsDataURL(file);
    });
  }
};

const handleFileUpdate = (event) => {
  const files = event.target.files;
  if (files.length) {
    Array.from(files).forEach(file => {
      const reader = new FileReader();
      reader.onload = (e) => {
        editImages.value.push({ file, url: e.target.result });
      };
      reader.readAsDataURL(file);
    });
  }
  // console.log(editImages.value);
};

const getImageSrc = (image) => {
  // 如果是字符串类型，直接返回该字符串作为 URL
  if (typeof image === 'string') {
    return `http://localhost:8001${image}`;
  }
  // 如果是 File 类型，使用生成一个临时的图片 URL
  else {
    return image.url;
  }
}

// 移除预览图片
const removeImage = (index, type) => {
  if (type === 'add') {
    previewImages.value.splice(index, 1);
  } else if (type === 'edit') {
    editImages.value.splice(index, 1);
  }
};

// 发表说说
const submitEmotion = async () => {
  if (!addContent.value.trim() && !previewImages.value.length) {
    console.log("缺少内容");
    return;
  }

  const formData = new FormData();
  formData.append('content', addContent.value);
  formData.append('limit', addLimit.value);
  
  try {
    const response = await axios.post('http://localhost:8001/api/admin/addEmotion/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    
    const newformData = new FormData();  
    newformData.append('emotionId', response.data.emotionId)
    previewImages.value.forEach(({ file }) => {
      newformData.append('images[]', file);
    });
    await axios.post('http://localhost:8001/api/admin/addEmotionMedia/', newformData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
      
    showModalAdd.value = false;
    addContent.value = '';
    previewImages.value = [];
  } catch (error) {
    console.error('上传失败', error);
  }
  fetchEmotions();
};

// 修改说说
const updateEmotion = async () => {
  const formData = new FormData();
  formData.append('emotionId', currentEmotion.value.id);
  formData.append('content', currentEmotion.valuecontent);
  formData.append('limit', currentEmotion.value.limit);
  editImages.value.forEach((image) => {
    formData.append('images[]', image);
  });
  editImages.value.forEach(({ file }) => {
    formData.append('newimages[]', file);
  });
  
  try {
    await axios.post('http://localhost:8001/api/admin/updateEmotion/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    
    showModalEdit.value = false;
    currentEmotion = '';
    editImages.value = [];
    fetchEmotions();
  } catch (error) {
    console.error('修改失败', error);
  }
}

const editEmotion = async (emotion) => {
  currentEmotion.value = { ...emotion };
  try {
    const response = await axios.get('http://localhost:8001/api/admin/emotionDetail/', {
      params: { emotionId: emotion.id }
    });
    editImages.value = response.data.media_files;
    // console.log(editImages.value);
  } catch (error) {
    console.error('获取失败', error);
  }
  showModalEdit.value = true;
}

// 分页跳转
function goToPage(newPage) {
  if (newPage >= 1 && newPage <= totalPages.value) {
    page.value = newPage;
    fetchEmotions();
  }
}
</script>

<style>
.media-header {
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

.custom-checkbox input[type="checkbox"] {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 2px solid #007bff;
  position: relative;
  margin-right: 10px; 
  cursor: pointer;  
  transition: background-color 0.3s, border-color 0.3s;
}

.custom-checkbox input[type="checkbox"]:checked {
  background-color: #007bff;
  border-color: #007bff;  
}

.custom-checkbox input[type="checkbox"]:checked::after {
  content: '';           
  position: absolute;
  top: 50%;                   
  left: 50%;               
  width: 8px;
  height: 8px;
  border-left: 2px solid white;
  border-bottom: 2px solid white;
  transform: translate(-50%, -50%) rotate(-45deg);
}

.custom-checkbox {
  display: flex;
  align-items: center;
  font-size: 12px; 
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

/* Adjust baseOption to align buttons to the right */
.baseOption {
  margin-left: auto; /* Push the buttons to the right */
  display: flex;
  gap: 10px;
}

.addemotion-btn, .deleteemotion-btn {
  padding: 5px 12px;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
}

.addemotion-btn {
  background-color: #007bff;
  color: white;
  border: none;
}

.addemotion-btn:hover {
  background-color: #0056b3;
}

.deleteemotion-btn {
  color: grey;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
}

.deleteemotion-btn:hover {
  background-color: #e0e0e0;
}

.table-container {
  margin: 20px;
  margin-left: 0;
  width: 80%; /* 确保容器宽度为100% */
}

table {
  width: 100%; /* 表格宽度占满容器 */
  border-collapse: collapse; /* 合并边框 */
  text-align: center; /* 表格内容居中 */
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
}

.checkbox-column {
  width: 40px;
  text-align: center;
}

.id-column {
  width: 50px;
}

.content-column {
  width: 650px;
}

.time-column {
  width: 160px;
}

.action-column {
  width: 120px;
}

.submit-edit-base-btn {
  /* width: 100%; */
  margin-top: 20px;
  padding: 5px 12px;
  font-size: 0.85em;
  border-radius: 4px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

.pagination {
  text-align: center;
}

.pagination button {
  padding: 5px 15px;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #ddd;
  cursor: not-allowed;
}

.image-preview {
  display: grid;
  grid-template-columns: repeat(3, 100px);
  gap: 10px;
  margin-top: 10px;
}

.image-container {
  position: relative;
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #ddd;
  border-radius: 5px;
  overflow: hidden;
}

.preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 14px;
  cursor: pointer;
}
</style>
