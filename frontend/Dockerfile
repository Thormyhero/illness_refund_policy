FROM node:18-alpine

WORKDIR /app

# 安装依赖
COPY package*.json ./
RUN npm install

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 5173

# 运行开发服务器（--host 支持外部访问）
CMD ["npm", "run", "dev", "--", "--host"]
