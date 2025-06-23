<template>
  <div class="message-header">
    <div class='section'>
      <label for="uid">用户UID：</label>
      <input id="uid" type="text" v-model="uid" placeholder="请输入待查询用户的UID"/>
    </div>

    <div class="section">
      <button class="search-btn" @click="searchOpition">搜索</button>
      <button class="reset-btn" @click="resetOption">重置</button>
    </div>

    <div class="baseOption">
      <button class="deletephoto-btn" @click="() => deleteSelectedMessages()">删除留言</button>
    </div>
  </div>

  <!-- 留言列表 -->
  <div class="table-container">
    <table>
      <!-- 表头 -->
      <thead>
        <tr>
          <th class="checkbox-column">
            <input type="checkbox" v-model="selectAll" @change="toggleSelectAll" />
          </th>
          <th class="id-column">编号</th>
          <th class="content-column">留言</th>
          <th class="uid-column">用户UID</th>
          <th class="name-column">用户名</th>
          <th class="time-column">创建时间</th>
          <th class="action-column">操作</th>
        </tr>
      </thead>

      <!-- 表体 -->
      <tbody>
        <tr v-for="(message, index) in messages" :key="message.id">
          <td class="checkbox-column">
            <input type="checkbox" v-model="message.selected" />
          </td>
          <td class="id-column">{{ message.id }}</td>
          <td class="content-column">{{ message.content }}</td>
          <td class="uid-column">{{ message.uid }}</td>
          <td class="name-column">{{ message.name }}</td>
          <td class="time-column">{{ message.created_at }}</td>
          <td class="action-column">
            <button @click="messageDetail(message)" class="delete-option">查看</button>
            <button @click="deleteSelectedMessages([message.id])" class="delete-option">删除</button>
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

  <!-- 模态窗口-查看留言 -->
  <changeModal v-model:visible="showModal" title="查看具体的留言内容">    
    <!-- 留言id -->
    <div class="form-item">
      <label for="id">编号:</label>
      <input id="id" type="text" v-model="currentMessage.id" disabled />
    </div>

    <!-- 内容 -->
    <div class="form-item">
      <label for="content">内容:</label>
      <textarea
        id="content"
        v-model="currentMessage.content"
        rows="4"
        disabled 
      ></textarea>
    </div>

    <!-- 用户UID -->
    <div class="form-item">
      <label for="uid">用户UID:</label>
      <input id="uid" type="text" v-model="currentMessage.uid" disabled />
    </div>

    <!-- 用户名 -->
    <div class="form-item">
      <label for="name">用户名:</label>
      <input id="name" type="text" v-model="currentMessage.name" disabled />
    </div>

    <!-- 创建时间 -->
    <div class="form-item">
      <label for="created_at">创建时间:</label>
      <input id="created_at" type="text" v-model="currentMessage.created_at" disabled />
    </div>
  </changeModal>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ElMessageBox, ElMessage } from 'element-plus';
import axios from "axios";
import changeModal from '@/adminPage/components/changeModal.vue';

const uid = ref("");
const messages = ref([]);
const currentMessage = ref({});

const page = ref(1); // 当前页数
const totalPages = ref(1); // 总页数

const showModal = ref(false);
const selectAll = ref(false);

onMounted(() => {
  fetchMessages();
});

// 切换全选/全不选
function toggleSelectAll() {
  messages.value.forEach(message => {
    message.selected = selectAll.value;
  });
}

// 搜索选项
function searchOpition() {
  page.value = 1;
  fetchMessages();
}

// 重置搜素选项
function resetOption() {
  uid.value = "";
}

const messageDetail = async (message) => {
  currentMessage.value = { ...message };
  showModal.value = true;
}

const fetchMessages = async () => {
  try {
    // 组装查询参数
    const params = {
      page: page.value, // 当前页数
    };
    if (uid.value) {
      params.uid = uid.value;
    }
    const response = await axios.get("http://localhost:8001/api/admin/searchMessages/", {
      params, // Axios 会自动将对象转换为查询字符串
    });
    if (response.status === 200) {
      // 按后端返回的数据格式直接处理
      messages.value = response.data.results.map((message) => ({
        id: message.id,
        content: message.content,
        name: message.user_name,
        uid: message.user_uid,
        selected: false,
        created_at: message.created_at,
      }));
      // 更新总页数
      totalPages.value = Math.ceil(response.data.count / response.data.page_size);
    } else {
      console.error("后端数据格式不正确：", response.data);
    }
  } catch (error) {
    ElMessage.error(error.response.data.error);
    console.error("获取留言列表失败：", error);
  }
}

const deleteSelectedMessages = async (selectedMessages = null) => {
  if (!selectedMessages) {
    selectedMessages = messages.value.filter(message => message.selected).map(message => message.id);
  }
  if (selectedMessages.length === 0) {
    ElMessage.warning("请先选择要删除的留言！");
    return;
  }

  // 使用 ElMessageBox 弹出确认框
  ElMessageBox.confirm(
    '确定要删除这些留言吗？\n删除相册以后留言无法找回。',
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
        const response = await axios.post("http://localhost:8001/api/admin/deleteMessages/", {
          ids: selectedMessages
        });

        if (response.status === 200) {
          ElMessage.success("删除成功！");
          fetchMessages(); // 刷新当前页
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
  fetchMessages();
}

// 分页跳转
function goToPage(newPage) {
  if (newPage >= 1 && newPage <= totalPages.value) {
    page.value = newPage;
    fetchMessages();
  }
}
</script>

<style>
.message-header {
  padding-right: 20%;
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: center;
  justify-content: space-between;
}

.baseOption {
  margin-left: auto; /* Push the buttons to the right */
  display: flex;
  gap: 10px;
}

.deletephoto-btn {
  padding: 5px 12px;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
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
  width: 80%;
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
  width: 300px;
}

.name-column {
  width: 120px;
}

.uid-column {
  width: 120px;
}

.time-column {
  width: 160px;
}

.action-column {
  width: 130px;
  text-align: center;
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