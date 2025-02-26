<template>
  <div class="baseOption">
    <button class="addalbum-btn" @click="addAlbum">添加相册</button>
    <button class="deletealbum-btn" @click="() => deleteSelectedAlbums()">删除相册</button>
    <button class="flush-btn" @click="fetchAlbums">刷新</button>
  </div>

  <!-- 相册列表 -->
  <div class="table-container">
    <table>
      <!-- 表头 -->
      <thead>
        <tr>
          <th class="checkbox-column">
            <input type="checkbox" v-model="selectAll" @change="toggleSelectAll" />
          </th>
          <th class="id-column">编号</th>
          <th class="name-column">相册名</th>
          <th class="text-column">简介</th>
          <th class="count-column">相片数量</th>
          <th class="time-column">创建时间</th>
          <th class="time-column">更新时间</th>
          <th class="action-column">操作</th>
        </tr>
      </thead>

      <!-- 表体 -->
      <tbody>
        <tr v-for="(album, index) in albums" :key="album.id">
          <td class="checkbox-column">
            <input type="checkbox" v-model="album.selected" />
          </td>
          <td class="id-column">{{ album.id }}</td>
          <td class="name-column">{{ album.name }}</td>
          <td class="text-column">{{ album.description }}</td>
          <td class="count-column">{{ album.count }}</td>
          <td class="time-column">{{ album.created_at }}</td>
          <td class="time-column">{{ album.updated_at }}</td>
          <td class="action-column">
            <button @click="editalbum(album)" class="edit-option">编辑</button>
            <button @click="deleteSelectedAlbums([album.id])" class="delete-option">删除</button>
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

  <!-- 模态窗口-添加相册 -->
  <changeModal v-model:visible="showModalAdd" title="相册添加窗口">
    <form @submit.prevent="saveChanges">
      
      <!-- 相册名称 -->
      <div class="form-item">
        <label for="name">相册名:</label>
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

      <!-- 保存按钮 -->
      <button type="submit" class="submit-edit-base-btn" @click="add_Album()">添加相册</button>
    </form>
  </changeModal>

  <!-- 模态窗口-修改相册 -->
  <changeModal v-model:visible="showModalEdit" title="相册信息修改窗口">
    <form @submit.prevent="saveChanges">
      
      <!-- 相册编号 -->
      <div class="form-item">
        <label for="id">相册编号:</label>
        <input id="id" type="text" v-model="currentAlbum.id" disabled />
      </div>

      <!-- 相册名称 -->
      <div class="form-item">
        <label for="name">相册名:</label>
        <input id="name" type="text" v-model="currentAlbum.name" />
      </div>

      <!-- 介绍 -->
      <div class="form-item">
        <label for="description">介绍:</label>
        <textarea
          id="description"
          v-model="currentAlbum.description"
          rows="4"
        ></textarea>
      </div>

      <!-- 文章数目 -->
      <div class="form-item">
        <label for="count">文章数目:</label>
        <input id="count" type="text" v-model="currentAlbum.count" disabled />
      </div>

      <!-- 创建时间 -->
      <div class="form-item">
        <label for="created_at">创建时间:</label>
        <input id="created_at" type="text" v-model="currentAlbum.created_at" disabled />
      </div>

      <!-- 最后更新时间 -->
      <div class="form-item">
        <label for="updated_at">最后更新时间:</label>
        <input id="updated_at" type="text" v-model="currentAlbum.updated_at" disabled />
      </div>

      <!-- 保存按钮 -->
      <button type="submit" class="submit-edit-base-btn" @click="edit_Album()">保存修改</button>
    </form>
  </changeModal>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ElMessageBox, ElMessage } from 'element-plus';
import axios from "axios";
import changeModal from '@/adminPage/components/changeModal.vue';

const albums = ref([]);
const addName = ref("");
const addDescription = ref("");
const currentAlbum = ref({});

const page = ref(1); // 当前页数
const totalPages = ref(1); // 总页数

const showModalAdd = ref(false);
const showModalEdit = ref(false);
// 全选框的状态
const selectAll = ref(false);

onMounted(() => {
  fetchAlbums();
});

// 切换全选/全不选
function toggleSelectAll() {
  albums.value.forEach(album => {
    album.selected = selectAll.value;
  });
}

const addAlbum = async () => {
  showModalAdd.value = true;
}

const fetchAlbums = async () => {
  try {
    // 组装查询参数
    const params = {
      page: page.value, // 当前页数
    };
    const response = await axios.get("http://localhost:8001/api/admin/searchAlbum/", {
    params, // Axios 会自动将对象转换为查询字符串
    });
    if (response.status === 200) {
      // 按后端返回的数据格式直接处理
      albums.value = response.data.results.map((album) => ({
        id: album.id,
        name: album.name,
        description: album.description || '暂无描述', // 若 summary 为 null，则显示“暂无描述”
        count: album.count,
        selected: false, // 前端状态
        created_at: album.created_at,  // 创建时间
        updated_at: album.updated_at, // 更新时间
      }));
      // 更新总页数
      totalPages.value = Math.ceil(response.data.count / 6);
    } else {
      console.error("后端数据格式不正确：", response.data);
    }
  } catch (error) {
    console.error("获取相册列表失败：", error);
  }
}

async function add_Album() {
  try {
    const formData = new FormData();
    formData.append('name', addName.value);
    formData.append('description', addDescription.value);

    const response = await axios.post('http://localhost:8001/api/admin/addAlbum/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',  // 告诉服务器这次请求是上传文件
    },
    });

    if (response.status === 201) {
      // 上传成功，获取返回的 id
      console.log('相册创建成功');
    } else {
      console.log(response.status);
      console.error('相册创建失败:', response.data);
    }
  } catch (error) {
    console.error('添加相册出错:', error);
  }
  // 刷新当前页面
  fetchAlbums();

  showModalAdd.value = false;
  addName.value = "";
  addDescription.value = "";
}

const deleteSelectedAlbums = async (selectedAlbums = null) => {
  if (!selectedAlbums) {
    selectedAlbums = albums.value.filter(album => album.selected).map(album => album.id);
  }
  if (selectedAlbums.length === 0) {
    ElMessage.warning("请先选择要删除的相片！");
    return;
  }

  // 使用 ElMessageBox 弹出确认框
  ElMessageBox.confirm(
    '确定要删除这些相册吗？\n删除相册以后相片不会消失。',
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
        const response = await axios.post("http://localhost:8001/api/admin/deleteAlbums/", {
          ids: selectedAlbums
        });

        if (response.status === 200) {
          ElMessage.success("删除成功！");
          fetchAlbums(); // 刷新当前页
        } else {
          ElMessage.error("删除失败！");
        }
      } catch (error) {
        console.error("删除相册失败：", error);
        ElMessage.error("删除失败！");
      }
    })
    .catch(() => {
      // 取消删除
      console.log("用户取消删除操作");
    });
}

async function edit_Album() {
  try {
    const formData = new FormData();
    formData.append('id', currentAlbum.value.id);
    formData.append('name', currentAlbum.value.name);
    formData.append('description', currentAlbum.value.description);

    const response = await axios.post('http://localhost:8001/api/admin/updateAlbum/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',  // 告诉服务器这次请求是上传文件
    },
    });
    if (response.status === 200) {
      // 上传成功，获取返回的 id
      console.log('相册修改成功');
    } else {
      console.log(response.status);
      console.error('相册修改失败:', response.data);
    }
  } catch (error) {
    console.error('修改相册出错:', error);
  }

  fetchAlbums();
  showModalEdit.value = false;
}

const editalbum = async (album) => {
  currentAlbum.value = { ...album };
  showModalEdit.value = true;
}

// 分页跳转
function goToPage(newPage) {
  if (newPage >= 1 && newPage <= totalPages.value) {
    page.value = newPage;
    fetchAlbums();
  }
}
</script>

<style>
.baseOption {
  margin-left: auto; /* Push the buttons to the right */
  display: flex;
  gap: 10px;
}

.addalbum-btn, .deletealbum-btn, .flush-btn {
  padding: 5px 12px;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
}

.addalbum-btn {
  background-color: #007bff;
  color: white;
  border: none;
}

.addalbum-btn:hover {
  background-color: #0056b3;
}

.deletealbum-btn {
  color: grey;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
}

.deletealbum-btn:hover {
  background-color: #e0e0e0;
}

.flush-btn {
  background-color: rgb(0, 255, 115);
  color: rgb(180, 130, 5);
  border: 1px solid #ccc;
}

.flush-btn:hover {
  background-color: rgb(2, 228, 104);
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