# 病退政策管理系统 - Phase 1 完整系统

完整的病退政策库构建、版本管理、和多AI接入系统。

## 🎯 项目概述

这是一个**生产级别**的病退政策管理系统，包含：

✅ **后端API服务** - FastAPI + SQLite
✅ **前端Web应用** - Vue 3 + Pinia
✅ **完整版本管理** - 政策快照 + 回滚机制
✅ **操作审计日志** - 完整的修改历史
✅ **实时同步准备** - WebSocket支持框架
✅ **多AI接入支持** - Webhook API设计

---

## 🚀 快速开始 (5分钟)

### 方式1: 本地开发 (推荐)

#### 1️⃣ 启动后端

```bash
cd backend
pip install -r requirements.txt
python app.py
```

输出示例：
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
✓ API Server Started
```

#### 2️⃣ 启动前端

```bash
cd frontend
npm install
npm run dev
```

输出示例：
```
  ➜  Local:   http://localhost:5173/
```

#### 3️⃣ 访问应用

打开浏览器访问 **http://localhost:5173**

#### 4️⃣ 导入测试数据 (可选)

```bash
cd backend
python test_api.py
```

这会创建亚航政策和6种材料要求。

---

### 方式2: Docker Compose (一键启动)

```bash
docker-compose up
```

- API: http://localhost:8000
- Web: http://localhost:5173
- API文档: http://localhost:8000/docs

---

## 📖 系统架构

```
┌─────────────────────────────────────────┐
│         前端 (Vue 3 + Pinia)            │
│  http://localhost:5173                  │
└──────────────────┬──────────────────────┘
                   │ WebSocket/REST
┌──────────────────┴──────────────────────┐
│      后端 API (FastAPI)                 │
│  http://localhost:8000                  │
│  /api/policies, /api/versions etc       │
└──────────────────┬──────────────────────┘
                   │ SQLAlchemy ORM
┌──────────────────┴──────────────────────┐
│     数据库 (SQLite)                     │
│  data/policies.db                       │
└─────────────────────────────────────────┘
```

---

## 📋 功能清单

### Phase 1 已完成

- ✅ 数据模型设计 (Policy/Version/Material/AuditLog)
- ✅ 后端CRUD接口 (创建/查询/更新/删除政策)
- ✅ 版本管理系统 (快照/回滚/Diff)
- ✅ 操作审计日志 (完整追踪)
- ✅ 前端UI页面
  - ✅ 政策检索与展示
  - ✅ 版本管理与回滚
  - ✅ 系统统计
- ✅ API文档 (Swagger + ReDoc)
- ✅ 测试脚本

### Phase 2 准备中

- 🔄 WebSocket 实时同步
- 🔄 Webhook 多AI接入
- 🔄  政策导入/导出
- 🔄  高级搜索和过滤

---

## 🔗 API快速参考

### 政策管理

```bash
# 获取政策列表
curl http://localhost:8000/api/policies

# 获取单个政策
curl http://localhost:8000/api/policies/1

# 创建政策
curl -X POST http://localhost:8000/api/policies \
  -H "Content-Type: application/json" \
  -d '{
    "airline_code": "AK",
    "airline_name": "AirAsia",
    "ticket_desk_type": "all"
  }'

# 更新政策
curl -X PUT http://localhost:8000/api/policies/1 \
  -H "Content-Type: application/json" \
  -d '{"raw_policy": "..."}'
```

### 版本管理

```bash
# 获取版本历史
curl http://localhost:8000/api/policies/1/versions

# 回滚到指定版本
curl -X POST http://localhost:8000/api/policies/1/versions/5/rollback
```

### 查看完整API文档

访问 http://localhost:8000/docs (Swagger UI)

---

## 📁 项目结构

```
policy-system/
├── backend/
│   ├── app.py              # FastAPI应用
│   ├── models.py           # SQLAlchemy模型
│   ├── schemas.py          # Pydantic验证模型
│   ├── services.py         # 业务逻辑
│   ├── database.py         # 数据库连接
│   ├── test_api.py         # 测试脚本
│   ├── requirements.txt    # 依赖
│   ├── Dockerfile          # Docker镜像
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── main.js         # 入口
│   │   ├── App.vue         # 根组件
│   │   ├── components/     # 页面组件
│   │   ├── services/       # API服务
│   │   └── stores/         # Pinia状态管理
│   ├── index.html          # HTML模板
│   ├── vite.config.js      # Vite配置
│   ├── package.json
│   ├── Dockerfile
│   └── README.md
│
├── data/
│   └── airlines/           # 政策数据
│       └── AK/
│
├── docker-compose.yml      # Docker编排
└── README.md               # 此文件
```

---

## 🧪 测试

### 运行API测试

```bash
# 启动后端后，在新终端运行
cd backend
python test_api.py
```

输出示例：
```
============================================================
病退政策管理系统 - API 测试
============================================================

🔍 测试健康检查...
  ✓ {'status': 'healthy', 'timestamp': '...'}

📝 创建亚航病退政策...
  ✓ 政策创建成功 (ID: 1)

📋 添加材料要求 (政策ID: 1)...
  ✓ ticketing_document 添加成功
  ✓ medical_certificate 添加成功
  ...
```

### 手动测试

1. 打开 http://localhost:5173
2. 在 **政策检索** 页面查看创建的政策
3. 点击政策卡片查看详情
4. 在 **版本管理** 页面查看版本历史

---

## 📊 数据库Schema

### policies (政策表)
存储航司的病退政策原文和拆解数据

### materials (材料表)
存储政策的具体材料要求（证件、诊断证明等）

### versions (版本表)
存储每次政策变更的完整快照和元数据

### audit_logs (审计表)
记录所有操作（创建、更新、删除、回滚）

---

## 🔧 配置

### 环境变量

后端 (`backend/app.py`):
```python
DATABASE_URL = "sqlite:///./data/policies.db"  # 可改为 PostgreSQL
DEBUG = False  # 生产环境设为 False
```

### 修改API端口

```bash
# 后端
python app.py --port 8001

# 前端
npm run dev -- --port 5174
```

---

## 🐛 常见问题

### Q: 后端启动失败 "Address already in use"
A: 改变端口
```bash
python -m uvicorn app:app --port 8001
```

### Q: 前端无法连接后端
A: 检查CORS配置
1. 确保后端运行在 http://localhost:8000
2. 检查 `frontend/vite.config.js` 的proxy配置
3. 检查浏览器控制台错误信息

### Q: 数据库重置
A: 删除 `data/policies.db`，重启时会自动创建新数据库

### Q: 如何查看所有API?
A: 访问 http://localhost:8000/docs

---

## 📚 文档

- [后端 README](./backend/README.md) - API文档、测试、部署
- [前端 README](./frontend/README.md) - UI组件、开发指南
- [技术规划](../病退政策拆解/02-完整系统技术规划.md) - 架构设计

---

## 🚀 下一步 (Phase 2)

### WebSocket 实时同步
```javascript
// 后端政策更新后，前端实时接收
const ws = new WebSocket('ws://localhost:8000/ws/policies')
```

### Webhook 多AI接入
```bash
curl -X POST http://localhost:8000/api/webhooks/update \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "airline_code": "AK",
    "changes": {...}
  }'
```

### 政策导入/导出
- 导出当前政策库为JSON
- 导入JSON文件批量更新政策
- 冲突解决策略（Keep/Overwrite/Merge）

---

## 📞 支持和反馈

遇到问题？

1. 查看浏览器控制台错误信息
2. 检查API文档: http://localhost:8000/docs
3. 查看测试脚本: `backend/test_api.py`

---

## 📝 License

MIT License

---

## ✨ 系统亮点

🎯 **完整版本管理** - 任何时刻都可回滚到历史版本
📊 **操作审计追踪** - 记录谁在什么时间做了什么改动
🔄 **实时同步准备** - WebSocket框架已预留
🤖 **多AI接入支持** - Webhook API设计完成
📱 **响应式设计** - 桌面和移动端完美适配
⚡ **高性能架构** - FastAPI + Vue 3 性能优化

---

**快速开始: `cd backend && python app.py` + `cd frontend && npm run dev`**
