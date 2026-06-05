# 开发指南

## Phase 1 已完成

这个系统包含完整的后端API和前端UI，支持：
- ✅ 政策CRUD操作
- ✅ 版本管理和回滚
- ✅ 操作审计日志
- ✅ 前端UI展示
- ✅ API文档

## Phase 2 开发计划

### 1. WebSocket 实时同步 

添加实时政策更新推送功能。

**实现步骤：**
1. 后端：添加WebSocket路由
```python
# backend/app.py
from fastapi import WebSocket

@app.websocket("/ws/policies")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # 广播政策更新
```

2. 前端：连接WebSocket
```javascript
// frontend/src/services/websocket.js
const ws = new WebSocket('ws://localhost:8000/ws/policies')
ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  // 实时更新页面
}
```

3. 测试：修改政策后，所有连接的客户端都会收到更新

### 2. Webhook 多AI接入

添加外部AI系统更新政策的能力。

**实现步骤：**
1. 后端：实现Webhook验证和处理
```python
# backend/api/webhooks.py
from fastapi import Header
import hmac

@app.post("/api/webhooks/update")
async def webhook_update(
    data: dict,
    authorization: str = Header(None),
    x_signature: str = Header(None)
):
    # 验证签名
    # 应用变更
    # 广播更新
```

2. 生成API Key
```python
# 在管理界面生成、管理API Key
```

3. 测试：模拟AI系统调用
```bash
curl -X POST http://localhost:8000/api/webhooks/update \
  -H "Authorization: Bearer {token}" \
  -H "X-Signature: {signature}" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

### 3. 政策导入/导出

完善数据导入导出功能。

**实现步骤：**
1. 后端：实现导出端点
```python
@app.get("/api/export")
def export_policies():
    # 导出所有政策为JSON
```

2. 前端：实现导入UI
```vue
<!-- ImportExport.vue -->
<input type="file" @change="handleFileUpload" />
```

3. 实现冲突解决逻辑

### 4. 多语言支持

国际化前端和数据。

**实现步骤：**
1. 前端：集成i18n
```javascript
import i18n from 'vue-i18n'
```

2. 后端：支持多语言字段

3. 语言切换UI

---

## 代码规范

### 后端

**命名规范：**
- 类名：CamelCase (e.g., `PolicyService`)
- 函数：snake_case (e.g., `get_policy`)
- 常量：UPPER_SNAKE_CASE (e.g., `DATABASE_URL`)

**代码风格：**
- 使用类型注解
- 文档字符串（docstring）
- 异常处理

**示例：**
```python
def create_policy(db: Session, policy: PolicyCreate) -> Policy:
    """
    创建新政策
    
    Args:
        db: 数据库会话
        policy: 政策数据
        
    Returns:
        创建的政策对象
        
    Raises:
        HTTPException: 如果政策已存在
    """
    # 实现
```

### 前端

**命名规范：**
- 组件文件：PascalCase (e.g., `PolicySearch.vue`)
- 函数：camelCase (e.g., `handleClick`)
- 常量：UPPER_SNAKE_CASE (e.g., `API_BASE_URL`)

**代码风格：**
- 使用 `<script setup>` 语法
- Scoped样式
- 组件注释

**示例：**
```vue
<script setup>
/**
 * 政策搜索组件
 * 提供搜索和过滤功能
 */
import { ref } from 'vue'

const handleSearch = () => {
  // 实现
}
</script>
```

---

## 测试

### 后端测试

```bash
# 运行单个测试
pytest backend/tests/test_policies.py::test_create_policy

# 运行全部测试
pytest backend/tests/

# 生成覆盖率报告
pytest --cov=backend backend/tests/
```

### 前端测试

```bash
# 运行单元测试
npm run test

# 生成覆盖率报告
npm run test:coverage

# E2E测试
npm run test:e2e
```

---

## 调试

### 后端

```python
# 启用日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 调试模式
# 在app.py中：DEBUG = True
```

### 前端

```javascript
// Vue DevTools 浏览器扩展
// 调试状态管理：查看Pinia store

// 网络调试
// 打开浏览器开发者工具 -> Network 标签页
```

---

## 性能优化

### 后端

- 使用数据库索引
- 查询优化（避免N+1问题）
- 缓存热点数据

```python
# 示例：添加索引
class Policy(Base):
    airline_code = Column(String(10), index=True)
```

### 前端

- 懒加载组件
- 虚拟列表（大数据列表）
- 图片优化

```javascript
// 动态导入
const PolicyDetail = defineAsyncComponent(
  () => import('./PolicyDetail.vue')
)
```

---

## 部署

### 本地开发

```bash
# 后端
cd backend
python app.py

# 前端
cd frontend
npm run dev
```

### Docker部署

```bash
docker-compose up
```

### 云部署

#### Heroku
```bash
git push heroku main
```

#### AWS/Azure/GCP
配置CI/CD流程自动部署

---

## 常见任务

### 添加新的API端点

1. 在 `backend/models.py` 添加模型字段（如需要）
2. 在 `backend/schemas.py` 添加验证模型
3. 在 `backend/services.py` 添加业务逻辑
4. 在 `backend/app.py` 添加路由

```python
@app.post("/api/policies/{id}/duplicate")
def duplicate_policy(policy_id: int, db: Session = Depends(get_db)):
    # 实现
```

### 添加新的前端页面

1. 在 `frontend/src/components/` 创建新组件
2. 在 `frontend/src/App.vue` 添加导航
3. 添加对应的API调用
4. 添加状态管理（如需要）

```vue
<!-- NewPage.vue -->
<template>
  <div class="new-page">
    <!-- UI -->
  </div>
</template>

<script setup>
// 逻辑
</script>

<style scoped>
/* 样式 */
</style>
```

### 修改数据模型

1. 修改 `backend/models.py`
2. 创建数据库迁移（如使用Alembic）
3. 更新 `backend/schemas.py`
4. 更新相关API

---

## 问题排查

### 后端问题

| 问题 | 解决方案 |
|------|---------|
| 导入错误 | 确保所有依赖已安装：`pip install -r requirements.txt` |
| 数据库错误 | 删除 `data/policies.db` 重新初始化 |
| 端口被占用 | 改变端口或关闭占用端口的进程 |

### 前端问题

| 问题 | 解决方案 |
|------|---------|
| 模块未找到 | 运行 `npm install` |
| 样式不生效 | 清除浏览器缓存，检查选择器 |
| 后端连接失败 | 检查API代理配置，确保后端运行 |

---

## 贡献指南

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

---

## 联系方式

- Issues: 使用GitHub Issues报告问题
- 讨论: 在项目讨论区提问

---

**Happy Coding!** 🚀
