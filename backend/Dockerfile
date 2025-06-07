FROM python:3.12-slim

# 环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装依赖
RUN apt-get update && apt-get install -y \
    python3-dev \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config

# 工作目录
WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY backend /app