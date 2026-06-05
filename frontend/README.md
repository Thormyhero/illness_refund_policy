# 病退政策管理系统 - 前端 Vue3 应用

## 🚀 快速开始

### 环境要求
- Node.js 16.0+
- npm 8.0+

### 安装依赖

```bash
cd frontend
npm install
```

### 开发模式

```bash
npm run dev
```

应用会在 `http://localhost:5173` 启动

### 生产构建

```bash
npm run build
```

构建文件会生成在 `dist/` 目录

### 预览生产构建

```bash
npm run preview
```

---

## 📁 项目结构

```
frontend/
├── index.html           # HTML入口
├── package.json         # npm配置
├── vite.config.js       # Vite配置
└── src/
    ├── main.js          # 应用入口
    ├── App.vue          # 根组件
    ├── components/
    │   ├── PolicySearch.vue      # 政策检索页面
    │   ├── PolicyDetail.vue      # 政策详情modal
    │   ├── VersionManage.vue     # 版本管理页面
    │   ├── RollbackConfirm.vue   # 回滚确认modal
    │   └── StatsView.vue         # 统计页面
    ├── services/
    │   └── api.js                # API服务层
    └── stores/
        └── policyStore.js        # Pinia状态管理
```

---

## 🎨 功能页面

### 1. 📋 政策检索 (PolicySearch)
- 按航司和票台类型过滤政策
- 卡片式展示政策列表
- 点击卡片查看详细信息
- 实时搜索和筛选

### 2. 📖 政策详情 (PolicyDetail)
- 原文政策展示（可折叠）
- 结构化材料要求展示
- 材料详情（定义+简要规则）
- 复制功能
- 版本信息展示
- JSON导出功能

### 3. 📜 版本管理 (VersionManage)
- 版本时间线展示
- 按政策查询历史版本
- 版本Diff展示
- 一键回滚机制
- 操作审计追踪

### 4. 📊 统计信息 (StatsView)
- 系统统计卡片
- 功能特性列表
- 快速链接
- 下一步计划

---

## 🔌 API集成

### 后端API要求
- 基础URL: `http://localhost:8000`
- 所有API响应必须为JSON格式
- CORS已配置支持跨域请求

### 主要API端点

```javascript
// 政策
GET /api/policies              # 获取政策列表
GET /api/policies/:id          # 获取政策详情
POST /api/policies             # 创建政策
PUT /api/policies/:id          # 更新政策
DELETE /api/policies/:id       # 删除政策

// 材料
GET /api/policies/:id/materials
POST /api/policies/:id/materials
PUT /api/materials/:id
DELETE /api/materials/:id

// 版本
GET /api/policies/:id/versions
GET /api/versions/:id
POST /api/policies/:id/versions/:vid/rollback

// 其他
GET /api/stats                 # 统计信息
GET /health                    # 健康检查
```

---

## 🎯 核心特性

### 动画效果
- 页面进入/退出动画（`fadeIn`, `slideUp`）
- 卡片翻转动画（`cardSlideIn`）
- 版本时间线动画（`slideIn`）
- 模态框弹出动画

### 响应式设计
- 自适应网格布局
- 移动端优化
- 平板适配

### 用户体验
- 实时搜索和过滤
- 加载状态提示
- 错误提示
- 操作确认对话框

---

## 🛠️ 技术栈

| 库 | 版本 | 用途 |
|---|------|------|
| Vue | 3.3.4 | 前端框架 |
| Pinia | 2.1.6 | 状态管理 |
| Axios | 1.6.0 | HTTP客户端 |
| Vite | 5.0.0 | 构建工具 |

---

## 📝 开发指南

### 添加新组件

1. 在 `src/components/` 创建 `.vue` 文件
2. 编写 `<template>`, `<script setup>`, `<style scoped>`
3. 在 `App.vue` 或其他页面中导入使用

### 调用API

```javascript
import { policyAPI } from '@/services/api'

// 获取政策列表
const response = await policyAPI.list('AK', 'all')
```

### 状态管理

```javascript
import { usePolicyStore } from '@/stores/policyStore'

const store = usePolicyStore()
await store.fetchPolicies()
```

---

## 🚀 性能优化

- 使用 Vite 进行快速开发
- Vue 3 Composition API 优化渲染
- 懒加载模态框
- 虚拟列表支持（可扩展）

---

## 🔒 安全性

- XSS防护：Vue自动HTML转义
- CSRF保护：服务器配置
- 敏感数据：不存储在localStorage

---

## 📱 浏览器支持

- Chrome (最新)
- Firefox (最新)
- Safari (最新)
- Edge (最新)

不支持 IE11

---

## 🐛 故障排除

### 连接后端失败
- 确保后端运行在 `http://localhost:8000`
- 检查CORS配置
- 查看浏览器控制台错误信息

### 样式不生效
- 确保使用 `<style scoped>`
- 检查CSS类名是否正确
- 清理浏览器缓存

### 模态框显示问题
- 检查 `z-index` 值
- 确保父元素没有 `overflow: hidden`

---

## 📞 支持

遇到问题？请：
1. 检查浏览器控制台错误信息
2. 查看后端API文档
3. 查看组件代码注释

---

## 📝 License

MIT License
