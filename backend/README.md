# 病退政策管理系统 - 后端 API

## 🚀 快速开始

### 环境要求
- Python 3.10+
- pip

### 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 运行服务

```bash
python app.py
```

服务会在 `http://localhost:8000` 启动

### 查看 API 文档

启动后访问：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📋 核心功能

### 1. 政策管理

#### 创建政策
```bash
curl -X POST "http://localhost:8000/api/policies" \
  -H "Content-Type: application/json" \
  -d '{
    "airline_code": "AK",
    "airline_name": "AirAsia",
    "ticket_desk_type": "all",
    "raw_policy": "政策原文...",
    "breakdown_json": {...}
  }'
```

#### 查询政策
```bash
# 查询所有
curl "http://localhost:8000/api/policies"

# 按航司查询
curl "http://localhost:8000/api/policies?airline_code=AK"

# 获取单个
curl "http://localhost:8000/api/policies/1"
```

#### 更新政策
```bash
curl -X PUT "http://localhost:8000/api/policies/1?operator=bellali" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_policy": "更新的政策...",
    "breakdown_json": {...}
  }'
```

#### 删除政策
```bash
curl -X DELETE "http://localhost:8000/api/policies/1"
```

---

### 2. 材料管理

#### 添加材料
```bash
curl -X POST "http://localhost:8000/api/policies/1/materials" \
  -H "Content-Type: application/json" \
  -d '{
    "material_type": "medical_certificate",
    "definition": "医疗机构开具的诊断证明...",
    "simple_rules": ["纸质版", "需医生签字"],
    "detailed_config": {...}
  }'
```

#### 获取材料
```bash
curl "http://localhost:8000/api/policies/1/materials"
```

#### 更新材料
```bash
curl -X PUT "http://localhost:8000/api/materials/1" \
  -H "Content-Type: application/json" \
  -d '{
    "definition": "更新的定义...",
    "simple_rules": [...]
  }'
```

---

### 3. 版本管理

#### 获取版本历史
```bash
curl "http://localhost:8000/api/policies/1/versions"
```

#### 获取单个版本
```bash
curl "http://localhost:8000/api/versions/1"
```

#### 回滚政策
```bash
curl -X POST "http://localhost:8000/api/policies/1/versions/5/rollback?operator=bellali"
```

---

### 4. 审计日志

#### 获取审计日志
```bash
curl "http://localhost:8000/api/policies/1/audit-logs"
```

---

### 5. 统计信息

```bash
curl "http://localhost:8000/api/stats"
```

响应示例：
```json
{
  "total_policies": 1,
  "total_versions": 3,
  "total_airlines": 1,
  "timestamp": "2025-05-28T14:35:22.123456"
}
```

---

## 🧪 测试

运行测试脚本：

```bash
# 先启动API服务在另一个终端
python app.py

# 新终端中运行测试
python test_api.py
```

测试脚本会：
1. ✓ 检查健康状态
2. ✓ 创建亚航政策
3. ✓ 添加6种材料要求
4. ✓ 查询政策详情
5. ✓ 查询政策列表
6. ✓ 获取版本历史
7. ✓ 更新政策（创建新版本）
8. ✓ 查看审计日志
9. ✓ 获取系统统计

---

## 📁 项目结构

```
backend/
├── app.py              # FastAPI 应用主文件
├── models.py           # SQLAlchemy 数据模型
├── schemas.py          # Pydantic 数据校验模型
├── services.py         # 业务逻辑层
├── database.py         # 数据库连接和初始化
├── test_api.py         # API 测试脚本
└── requirements.txt    # 依赖列表
```

---

## 🔄 数据流程

```
前端请求
  ↓
FastAPI 路由
  ↓
Schemas 校验
  ↓
Services 业务逻辑
  ↓
Models ORM
  ↓
SQLite 数据库
  ↓
响应 JSON
```

---

## 📊 数据库Schema

### policies (政策表)
- `id`: 主键
- `airline_code`: 航司代码
- `airline_name`: 航司名称
- `ticket_desk_type`: 票台类型
- `raw_policy`: 原始政策文本
- `breakdown_json`: 拆解后的结构化数据
- `created_at`: 创建时间
- `updated_at`: 更新时间
- `current_version_id`: 当前版本ID

### materials (材料表)
- `id`: 主键
- `policy_id`: 政策ID
- `material_type`: 材料类型
- `definition`: 完整定义
- `simple_rules`: 简要规则
- `detailed_config`: 详细配置

### versions (版本表)
- `id`: 主键
- `policy_id`: 政策ID
- `version_number`: 版本号
- `version_tag`: 版本标签
- `changes_summary`: 变更摘要
- `changes_detail`: 变更详情
- `operator`: 操作者
- `operation_type`: 操作类型 (create/update/rollback)
- `policy_snapshot`: 快照
- `created_at`: 创建时间

### audit_logs (审计日志表)
- `id`: 主键
- `policy_id`: 政策ID
- `action`: 操作类型
- `operator`: 操作者
- `details`: 操作详情
- `created_at`: 创建时间

---

## 🔗 API 端点速查

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | /health | 健康检查 |
| POST | /api/policies | 创建政策 |
| GET | /api/policies | 查询政策列表 |
| GET | /api/policies/{id} | 获取政策详情 |
| PUT | /api/policies/{id} | 更新政策 |
| DELETE | /api/policies/{id} | 删除政策 |
| POST | /api/policies/{id}/materials | 添加材料 |
| GET | /api/policies/{id}/materials | 获取材料列表 |
| PUT | /api/materials/{id} | 更新材料 |
| DELETE | /api/materials/{id} | 删除材料 |
| GET | /api/policies/{id}/versions | 获取版本历史 |
| GET | /api/versions/{id} | 获取版本详情 |
| POST | /api/policies/{id}/versions/{vid}/rollback | 回滚版本 |
| GET | /api/policies/{id}/audit-logs | 获取审计日志 |
| GET | /api/stats | 获取统计信息 |

---

## 🛠️ 故障排除

### 端口被占用

如果 8000 端口被占用，可以修改运行命令：
```bash
uvicorn app:app --port 8001
```

### 数据库错误

如果数据库损坏，删除 `data/policies.db` 后重新运行会自动创建新数据库。

### 依赖安装失败

确保 Python 版本 ≥ 3.10：
```bash
python --version
```

---

## 📝 下一步

- [ ] Phase 2: 前端 Vue3 应用
- [ ] Phase 3: WebSocket 实时同步
- [ ] Phase 4: Webhook 多AI接入
