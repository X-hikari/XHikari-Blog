<template>
  <div class="media-header">
    <div class="section">
      <label for="type">媒体分类：</label>
      <select v-model="filetype" id="types">
        <option disabled value="">请选择</option>
        <option v-for="option in types" :key="option" :value="option">{{ option }}</option>
      </select>

      <div class="section">
        <label for="myCheckbox" class="custom-checkbox">
          <input type="checkbox" v-model="myCheckbox"> 是否使用
        </label>
      </div>

      <div class="section">
        <button class="search-btn" @click="searchOpition">搜索</button>
        <button class="reset-btn" @click="resetOption">重置</button>
      </div>
    </div>

    <div class="baseOption">
      <button class="deletephoto-btn" @click="() => deleteSelectedMedia()">删除媒体</button>
    </div>
  </div>

  <!-- 媒体列表 -->
  <div class="table-container">
    <table>
      <!-- 表头 -->
      <thead>
        <tr>
          <th class="checkbox-column">
            <input type="checkbox" v-model="selectAll" @change="toggleSelectAll" />
          </th>
          <th class="id-column">编号</th>
          <th class="cover-column">图片</th>
          <th class="name-column">文件名</th>
          <th class="type-column">文件类型</th>
          <th class="size-column">文件大小</th>
          <th class="time-column">上传时间</th>
          <th class="used-column">是否使用</th>
          <th class="action-column">操作</th>
        </tr>
      </thead>

      <!-- 表体 -->
      <tbody>
        <tr v-for="(media, index) in medias" :key="media.id">
          <td class="checkbox-column">
            <input type="checkbox" v-model="media.selected" />
          </td>
          <td class="id-column">{{ media.id }}</td>
          <td class="cover-column">
            <div class="cover-wrapper">
              <img v-bind:src="`http://localhost:8001${media.Url}`" />
            </div>
          </td>
          <td class="name-column">{{ media.name }}</td>
          <td class="type-column">{{ media.type }}</td>
          <td class="size-column">{{ media.size }}</td>
          <td class="time-column">{{ media.time }}</td>
          <td class="used-column">{{ media.used }}</td>
          <td class="action-column">
            <button @click="editMedia(media)" class="edit-option">编辑</button>
            <button @click="deleteSelectedMedia([media.id])" class="delete-option">删除</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- 模态窗口 -->
  <changeModal v-model:visible="showModal" title="媒体文件信息修改">
    <form @submit.prevent="saveChanges">
      <!-- ID -->
      <div class="form-item">
        <label for="id">ID:</label>
        <input id="id" type="text" v-model="currentMedia.id" disabled />
      </div>

      <!-- 图片 -->
      <div class="form-item">
        <label for="cover">图片:</label>
        <div class="background-section">
          <img v-bind:src="`http://localhost:8001${currentMedia.Url}`" class="background-preview" disabled >
        </div>
      </div>

      <!-- 文件名 -->
      <div class="form-item">
        <label for="name">文件名:</label>
        <input id="name" type="text" v-model="currentMedia.name" />
      </div>

      <!-- 类型 -->
      <div class="form-item">
        <label for="type">类型:</label>
        <input id="type" type="text" v-model="currentMedia.type" disabled />
      </div>
      
      <!-- 大小 -->
      <div class="form-item">
        <label for="size">大小:</label>
        <input id="size" type="text" v-model="currentMedia.size" disabled />
      </div>

      <!-- 创建时间 -->
      <div class="form-item">
        <label for="time">创建时间:</label>
        <input id="time" type="text" v-model="currentMedia.time" disabled />
      </div>
      
      <!-- 是否使用 -->
      <div class="form-item">
        <label for="used">是否使用:</label>
        <input id="used" type="text" v-model="currentMedia.used" disabled />
       </div>

      <!-- 保存按钮 -->
      <button type="submit" class="submit-edit-base-btn" @click="updateMedia">保存修改</button>
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
import { ref, onMounted } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus';
import axios from "axios";
import changeModal from "@/adminPage/components/changeModal.vue";

const isTypeFetched = ref(false);
const filetype = ref("");
const myCheckbox = ref(false);
const medias = ref([]);
const types = ref([]);
const currentMedia = ref({});

const page = ref(1); // 当前页数
const totalPages = ref(1); // 总页数

const showModal = ref(false);
const selectAll = ref(false);

onMounted(() => {
  fetchMedias();
});

// 切换全选/全不选
function toggleSelectAll() {
  medias.value.forEach(media => {
    media.selected = selectAll.value;
  });
}

const deleteSelectedMedia = async (selectedMeidas = null) => {
  if (!selectedMeidas) {
    selectedMeidas = medias.value.filter(media => media.selected).map(media => media.id);
  }
  if (selectedMeidas.length === 0) {
    ElMessage.warning("请先选择要删除的媒体！");
    return;
  }

  // 使用 ElMessageBox 弹出确认框
  ElMessageBox.confirm(
    '确定要删除这些媒体文件吗？\n删除的媒体文件无法找回。',
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
        const response = await axios.post("http://localhost:8001/api/admin/deleteMedias/", {
          ids: selectedMeidas
        });

        if (response.status === 200) {
          ElMessage.success("删除成功！");
          fetchMedias(); // 刷新当前页
        } else {
          ElMessage.error("删除失败！");
        }
      } catch (error) {
        console.error("删除媒体失败：", error);
        ElMessage.error("删除失败！");
      }
    })
    .catch(() => {
      // 取消删除
      console.log("用户取消删除操作");
    });
}

// 搜索选项
function searchOpition() {
  page.value = 1;
  fetchMedias();
}

// 重置搜素选项
function resetOption() {
  filetype.value = "";
  myCheckbox.value = false;
}

const fetchMedias = async () => {
  try {
    // 组装查询参数
    const params = {
      page: page.value, // 当前页数
    };
    if (filetype) {
      params.type = filetype.value;
    }
    if (myCheckbox) {
      params.used = myCheckbox.value
    }

    // 发起请求，带上查询参数
    const response = await axios.get("http://localhost:8001/api/admin/searchMedias/", {
      params, // Axios 会自动将对象转换为查询字符串
    });

    if (response.status === 200) {
      // 按后端返回的数据格式直接处理
      medias.value = response.data.results.map((media) => ({
        id: media.id,
        Url: media.file_url,
        name: media.file_name,
        type: media.file_type,
        size: media.file_size,
        selected: false, // 前端状态
        time: media.uploaded_at, // 更新时间
        used: media.used
      }));
      
      if (!isTypeFetched.value) {
        fetchMediatypes();
        isTypeFetched.value = true;
      }

      // 更新总页数
      totalPages.value = Math.ceil(response.data.count / 6);
    } else {
      console.error("后端数据格式不正确：", response.data);
    }
  } catch (error) {
    console.error("获取媒体图片列表失败：", error);
  }
};

const fetchMediatypes = async () => {
  try {
    if (medias.value) {
      // 创建一个 Set 来存储唯一的 type
      const typesSet = new Set();

      // 遍历 medias 数组，提取出每个 media 的 type 并放入 Set 中
      medias.value.forEach(media => {
        if (media.type) {
          typesSet.add(media.type); // 添加到 Set 中，重复的会被自动去掉
        }
      });
      types.value = typesSet;
      // console.log("所有的 type：", types);
    }
  } catch (error) {
    console.error("获取媒体类型失败：", error);
  }
};

const editMedia = async (media) => {
  currentMedia.value = { ...media };
  showModal.value = true;
}

async function updateMedia() {
  // console.log(currentMedia.value.name);
  try {
    const formData = new FormData();
    formData.append('id', currentMedia.value.id);
    if (currentMedia.value.name) {
      formData.append('name', currentMedia.value.name);
    }

    const response = await axios.post('http://localhost:8001/api/admin/updateMedia/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',  // 告诉服务器这次请求是上传文件
      },
    });

    if (response.status === 200) {
      // 上传成功，获取返回的 id
      console.log('媒体修改成功');
    } else {
      console.log(response.status);
      console.error('媒体修改失败:', response.data);
    }
  } catch (error) {
    console.error('修改媒体信息出错:', error);
  }

  // 刷新当前页面
  fetchMedias();

  showModal.value = false;
}

// 分页跳转
function goToPage(newPage) {
  if (newPage >= 1 && newPage <= totalPages.value) {
    page.value = newPage;
    fetchMedias();
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

.addphoto-btn, .deletephoto-btn {
  padding: 5px 12px;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
}

.addphoto-btn {
  background-color: #007bff;
  color: white;
  border: none;
}

.addphoto-btn:hover {
  background-color: #0056b3;
}

.deletephoto-btn {
  color: grey;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
}

.deletephoto-btn:hover {
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

.time-column {
  width: 160px;
}

.action-column {
  width: 120px;
}

.cover-wrapper img {
  width: 100px;
  height: auto;
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
</style>
