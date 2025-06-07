FROM node:20

WORKDIR /app

# 只复制 package.json，不复制 lock
COPY package.json ./

# 安装依赖，并让 npm 在 Linux 环境下生成正确的 lock
RUN npm install --include=dev --optional \
 && npm install @rollup/rollup-linux-x64-gnu --save-optional

# 复制剩余代码（包括 vite.config.js）
COPY . .

EXPOSE 3000

CMD ["npx", "vite"]
