<template>
  <div class="albumphotolist-header">
    <div class="section">
      <label for="albums">相册分类：</label>
      <select v-model="album" id="albums">
        <option disabled value="">请选择</option>
        <option v-for="option in allAlbums" :key="option" :value="option">{{ option }}</option>
      </select>
    </div>

    <div class="section">
      <button class="search-btn" @click="searchOpition">搜索</button>
      <button class="reset-btn" @click="resetOption">重置</button>
    </div>

    <div class="baseOption">
      <button class="addphoto-btn" @click="triggerFileInput">添加相片</button>
      <input type="file" ref="fileInput" @change="onFileChangeAndUpload" style="display: none;" />
      <button class="deletephoto-btn" @click="() => deleteSelectedAlbumPhotos()">删除相片</button>
    </div>
  </div>

  <!-- 相片列表 -->
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
          <th class="album-column">所属相册</th>
          <th class="time-column">上传时间</th>
          <th class="action-column">操作</th>
        </tr>
      </thead>

      <!-- 表体 -->
      <tbody>
        <tr v-for="(albumphoto, index) in albumphotos" :key="albumphoto.id">
          <td class="checkbox-column">
            <input type="checkbox" v-model="albumphoto.selected" />
          </td>
          <td class="id-column">{{ albumphoto.id }}</td>
          <td class="cover-column">
            <div class="cover-wrapper">
              <img v-bind:src="`http://localhost:8001${albumphoto.Url}`" />
            </div>
          </td>
          <td class="name-column">{{ albumphoto.name }}</td>
          <td class="type-column">{{ albumphoto.type }}</td>
          <td class="size-column">{{ albumphoto.size }}</td>
          <td class="album-column">{{ albumphoto.album }}</td>
          <td class="time-column">{{ albumphoto.time }}</td>
          <td class="action-column">
            <button @click="editalbumphoto(albumphoto)" class="edit-option">编辑</button>
            <button @click="deleteSelectedAlbumPhotos([albumphoto.id])" class="delete-option">删除</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- 模态窗口 -->
  <changeModal v-model:visible="showModal" title="图片信息修改">
    <form @submit.prevent="saveChanges">
      <!-- ID -->
      <div class="form-item">
        <label for="id">ID:</label>
        <input id="id" type="text" v-model="currentPhoto.id" disabled />
      </div>

      <!-- 图片 -->
      <div class="form-item">
        <label for="cover">图片:</label>
        <div class="background-section">
          <img v-bind:src="`http://localhost:8001${currentPhoto.Url}`" class="background-preview" disabled >
        </div>
      </div>

      <!-- 文件名 -->
      <div class="form-item">
        <label for="name">文件名:</label>
        <input id="name" type="text" v-model="currentPhoto.name" />
      </div>

      <!-- 类型 -->
      <div class="form-item">
        <label for="type">类型:</label>
        <input id="type" type="text" v-model="currentPhoto.type" disabled />
      </div>
      
      <!-- 大小 -->
      <div class="form-item">
        <label for="size">大小:</label>
        <input id="size" type="text" v-model="currentPhoto.size" disabled />
      </div>

      <!-- 所属相册 -->
      <div class="form-item">
        <label for="category">所属相册:</label>
        <select v-model="nowAlbum" id="allAlbums">
          <option value="">请选择相册</option>
          <option v-for="option in allAlbums" :key="option" :value="option">{{ option }}</option>
        </select>
      </div>

      <!-- 创建时间 -->
      <div class="form-item">
        <label for="time">创建时间:</label>
        <input id="time" type="text" v-model="currentPhoto.time" disabled />
      </div>

      <!-- 保存按钮 -->
      <button type="submit" class="submit-edit-base-btn" @click="updateAlbumPhoto">保存修改</button>
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

const album = ref("");
const allAlbums = ref([]);
const albumphotos = ref([]);
const currentPhoto = ref({});
const nowAlbum = ref("");

const fileInput = ref(null);
const selectedFile = ref(null);

const page = ref(1); // 当前页数
const totalPages = ref(1); // 总页数

const showModal = ref(false);
// 全选框的状态
const selectAll = ref(false);

onMounted(() => {
  fetchAlbumPhotos();
  fetchAlbumsName();
});

// 切换全选/全不选
function toggleSelectAll() {
  albumphotos.value.forEach(album => {
    album.selected = selectAll.value;
  });
}

// 触发文件选择框
const triggerFileInput = () => {
  fileInput.value.click();
};

// 选择文件并直接上传
const onFileChangeAndUpload = async (event) => {
  selectedFile.value = event.target.files[0]; // 获取选中的文件
  
  if (!selectedFile.value) {
    alert('请选择文件');
    return;
  }

  const formData = new FormData();
  formData.append('file', selectedFile.value); // 将文件附加到 FormData 对象
  formData.append('fileType', selectedFile.value.type); // 可以附加文件类型
  formData.append('fileSize', selectedFile.value.size); // 附加文件大小

  try {
    const response = await fetch("http://localhost:8001/api/admin/uploadAlbumPhoto/", {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      alert('上传成功');
    } else {
      alert('上传失败');
    }
  } catch (error) {
    console.error('上传失败', error);
    alert('上传失败');
  }

  fetchAlbumPhotos();
};

const deleteSelectedAlbumPhotos = async (selectedPhotos = null) => {
  if (!selectedPhotos) {
    selectedPhotos = albumphotos.value.filter(albumphoto => albumphoto.selected).map(albumphoto => albumphoto.id);
  }
  if (selectedPhotos.length === 0) {
    ElMessage.warning("请先选择要删除的相片！");
    return;
  }

  // 使用 ElMessageBox 弹出确认框
  ElMessageBox.confirm(
    '确定要删除这些相片吗？\n删除的相片无法找回。',
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
        const response = await axios.post("http://localhost:8001/api/admin/deleteAlbumPhotos/", {
          ids: selectedPhotos
        });

        if (response.status === 200) {
          ElMessage.success("删除成功！");
          fetchAlbumPhotos(); // 刷新当前页
        } else {
          ElMessage.error("删除失败！");
        }
      } catch (error) {
        console.error("删除相片失败：", error);
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
  fetchAlbumPhotos();
}

// 重置搜素选项
function resetOption() {
  album.value = "";
}

const fetchAlbumPhotos = async () => {
  try {
    // 组装查询参数
    const params = {
      page: page.value, // 当前页数
    };
    if (album.value) {
      params.album = album.value;
    }

    // 发起请求，带上查询参数
    const response = await axios.get("http://localhost:8001/api/admin/searchAlbumPhotos/", {
      params, // Axios 会自动将对象转换为查询字符串
    });

    if (response.status === 200) {
      // 按后端返回的数据格式直接处理
      albumphotos.value = response.data.results.map((albumphoto) => ({
        id: albumphoto.id,
        Url: albumphoto.file_url,
        name: albumphoto.file_name,
        type: albumphoto.file_type,
        size: albumphoto.file_size,
        album: albumphoto.album_name || '',
        selected: false, // 前端状态
        time: albumphoto.uploaded_at, // 更新时间
      }));
      // 更新总页数
      totalPages.value = Math.ceil(response.data.count / 6);
    } else {
      console.error("后端数据格式不正确：", response.data);
    }
  } catch (error) {
    console.error("获取相册图片列表失败：", error);
  }
};

const fetchAlbumsName = async () => {
  try {
    const response = await axios.get("http://localhost:8001/api/admin/searchAlbum/");
    if (response.status === 200) {
      allAlbums.value = response.data.map(album => album.name);
    } else {
      console.error("后端数据格式不正确：", response.data);
    }
  } catch (error) {
    console.error("获取相册名称失败：", error);
  }
}

const editalbumphoto = async (albumphoto) => {
  currentPhoto.value = { ...albumphoto };
  nowAlbum.value = albumphoto.album;
  showModal.value = true;
}

async function updateAlbumPhoto() {
  // console.log(currentPhoto.value.name);
  try {
    const formData = new FormData();
    formData.append('id', currentPhoto.value.id);
    if (currentPhoto.value.name) {
      formData.append('name', currentPhoto.value.name);
    }
    formData.append('album', nowAlbum.value);

    const response = await axios.post('http://localhost:8001/api/admin/updateAlbumPhoto/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',  // 告诉服务器这次请求是上传文件
      },
    });

    if (response.status === 200) {
      // 上传成功，获取返回的 id
      console.log('图片修改成功');
    } else {
      console.log(response.status);
      console.error('图片修改失败:', response.data);
    }
  } catch (error) {
    console.error('修改图片信息出错:', error);
  }

  // 刷新当前页面
  fetchAlbumPhotos();

  showModal.value = false;
}

// 分页跳转
function goToPage(newPage) {
  if (newPage >= 1 && newPage <= totalPages.value) {
    page.value = newPage;
    fetchAlbumPhotos();
  }
}
</script>

<style>
.albumphotolist-header {
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
