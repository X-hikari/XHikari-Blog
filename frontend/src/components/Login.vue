<template>
  <div class="login-container">
    <div class="login-box">
      <span class="close-btn" @click="closeLogin">×</span>
      <div class="title">登录框</div>
      <div class="name-pwd">
        <div class="section">
          <label for="username">
            <input type="text" id="username" v-model="username" placeholder="请输入您的用户名">
          </label>
        </div>
        <div class="section">
          <label for="userpwd">
            <input type="password" id="userpwd" v-model="password" placeholder="请输入您的密码">
          </label>
        </div>
        <button class="login-button" @click="login(username, password)">登录</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import sha256 from 'crypto-js/sha256';

const username = ref('');
const password = ref('');
const emit = defineEmits(['close']);

async function login(username, password) {
  const hashedPassword = sha256(password).toString();
  const params = new URLSearchParams();
  params.append("username", username);
  params.append("password", hashedPassword);

  const response = await fetch("http://localhost:8001/api/login/", {
    method: "POST",
    credentials: "include",  // 允许浏览器携带 Cookie
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",  // 使用表单格式
    },
    body: params.toString(),  // 将表单数据作为请求体
  });

  if (response.ok) {
    window.location.href = "/admin/";  // 登录后跳转到 Django Admin
  } else {
    // ElMessage.success("用户名或密码不正确");
    emit('close');
  }
}

const closeLogin = () => {
  emit('close'); // 触发关闭事件
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  background: rgba(0, 0, 0, 0.5);
  position: fixed;
  top: 0;
  left: 0;
}

.login-box {
  background: rgb(173, 216, 230);
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  width: 300px;
  position: relative;
}

.title {
  margin-bottom: 10px;
  font-size: 1.2em;
  font-weight: bold;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 15px;
  font-size: 1.5rem;
  cursor: pointer;
  color: #555;
}

.close-btn:hover {
  color: #000;
}

.section {
  margin-bottom: 1rem;
}

input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
}

.login-button {
  width: 30%;
  padding: 0.7rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.login-button:hover {
  background-color: #0056b3;
}
</style>
