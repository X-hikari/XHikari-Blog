<template>
  <div class="message-board">
    <!-- 在数据加载完成后再渲染 ShootingStars 组件 -->
    <ShootingStars v-if="!isLoading && messages.length > 0" :messages="messages" @click-star="showMessage" />

    <!-- 显示加载动画 -->
    <div v-if="isLoading" class="loading">
      <p>加载中...</p>
    </div>

    <div class="input-box">
      <textarea v-model="newMessage" placeholder="在夜空中留下你的足迹..." />
      <button @click="addMessage">发布</button>
    </div>

    <MessageCard
      v-if="selectedMessage"
      :message="selectedMessage"
      @close="selectedMessage = null"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import ShootingStars from "@/components/Message/ShootingStars.vue";

const messages = ref([]); // 存储留言
const newMessage = ref(""); // 输入框内容
const selectedMessage = ref(null); // 选中的留言
const isLoading = ref(true); // 数据加载状态，初始为 true

onMounted(() => {
  fetchMessages();
});

const fetchMessages = async () => {
  try {
    const response = await axios.get("http://localhost:8001/api/messages/");
    if (response.status === 200) {
      // 按后端返回的数据格式直接处理
      messages.value = response.data.results.map((message) => ({
        id: message.id,
        content: message.content,
        created_at: message.created_at,
        user: message.user_name,
      }));
    //   console.log(messages.value);
    } else {
      console.error("后端数据格式不正确：", response.data);
    }
  } catch (error) {
    console.error("获取留言列表失败：", error);
  } finally {
    isLoading.value = false; // 数据加载完成，关闭加载状态
  }
};

// 添加留言
const addMessage = async () => {
  if (!newMessage.value.trim()) return;

  try {
    const formData = new FormData();
    formData.append("content", newMessage.value);
    formData.append("user_id", "10000000"); // 需要替换成实际的用户ID

    const response = await axios.post("http://localhost:8001/api/addmessage/", formData, {
      headers: {
        "Content-Type": "multipart/form-data", // 告诉服务器这次请求是上传文件
      },
    });

    if (response.status === 201) {
      console.log("留言发布成功");
      // 在留言发布成功后再获取最新的留言数据
      fetchMessages();
    } else {
      console.error("留言发布失败:", response.data);
    }
  } catch (error) {
    console.error("留言发布出错:", error);
  }

  newMessage.value = ""; // 清空输入框
};

// 显示留言内容
const showMessage = (message) => {
  selectedMessage.value = message;
};
</script>

<style scoped>
.message-board::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("/MessageBackground.jpg");
  background-size: cover;
  background-position: top center;
  z-index: -1;
}

.message-board {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.input-box {
  position: absolute;
  bottom: 45%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.5);
  padding: 10px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  width: 300px;
}

textarea {
  width: 100%;
  height: 60px;
  background: transparent;
  color: white;
  border: none;
  outline: none;
  padding: 5px;
  resize: none;
}

button {
  margin-top: 5px;
  background: #ffcc00;
  border: none;
  padding: 5px;
  cursor: pointer;
}

.popup {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 15px;
  border-radius: 10px;
}

.loading {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  background: rgba(0, 0, 0, 0.7);
  padding: 20px;
  border-radius: 10px;
}
</style>
