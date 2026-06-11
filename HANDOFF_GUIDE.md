# 🎓 项目移交指南 - 适合 AI 继续开发

## 快速概览

**项目**: 病退政策管理系统  
**状态**: 功能完整，可持续添加政策  
**前端**: https://illnessrefund.netlify.app  
**后端**: https://illnessrefundpolicy-production.up.railway.app  

---

## 开发中遇到的 9 大卡点（已解决）

### 1. Netlify BOM 编码问题
- **症状**: netlify.toml 无法解析
- **解决**: 删除 UTF-8 BOM (`tail -c +4`)

### 2. 前后端连接失败
- **症状**: 404 错误
- **解决**: Netlify 环境变量设置 `VITE_API_BASE`

### 3. Vue SFC 编译错误
- **症状**: Invalid end tag at line 561
- **解决**: 删除重复的模板块（536 行）

### 4. SQLAlchemy 关系映射
- **症状**: "Cannot determine join condition"
- **解决**: 移除循环外键，添加 `foreign_keys` 参数

### 5. 字段长度溢出
- **症状**: String(10) 不够放"FD/XJ/D7/AK/QZ/Z2/KT"
- **解决**: 改为 String(100)

### 6. 数据随机丢失
- **症状**: SQLite 在容器内存中
- **解决**: 配置 PostgreSQL

### 7. ImportError init_db 缺失
- **症状**: 找不到 init_db 函数
- **解决**: 添加回函数到 database.py

### 8. PowerShell UTF-8 编码
- **症状**: 中文显示为 ????
- **解决**: 用 Python 脚本替代 PowerShell

### 9. 数据和代码混淆
- **症状**: 每次添加政策都需要重新部署
- **解决**: 创建独立 CLI 工具 (add_policy_cli.py)

---

## 关键工作流程

### ✅ 添加政策（正确方式 - 不改代码）

```bash
python add_policy_cli.py --code "MU" --name "中国东方航空" --refund "支持"
```

**三种方式**:
1. 交互式: `python add_policy_cli.py`
2. 命令行: `python add_policy_cli.py --code "..." --name "..."`
3. 批量: `python add_policy_cli.py batch`

### ❌ 错误方式 - 不要这样做

```python
# 不要在 app.py 启动时硬编码数据
@app.on_event("startup")
def startup():
    db.add(Policy(...))  # 这会导致重复部署时重复添加
```

---

## 政策拆解格式（4 步）

### 输入：航司原文政策

### 第 1-4 步：按标准格式拆解

```json
{
  "airline_code": "FD/XJ/D7/AK/QZ/Z2/KT",
  "airline_name": "亚航集团",
  "ticket_desk_type": "all",
  "breakdown_json": {
    "applicability": {
      "refund": "支持(条件)",
      "rebooking": "否"
    },
    "time_limits": {
      "cancel_seat": true,
      "advance_hours": "起飞前",
      "material_deadline": "客票有效期内"
    }
  }
}
```

### 材料要求（6 种）

| 类型 | 代码 |
|------|------|
| 购票证件 | ticketing_document |
| 诊断证明 | medical_certificate |
| 住院证明 | hospital_records |
| 检查报告 | inspection_report |
| 医疗发票 | medical_invoice |
| 陪同人证明 | companion_proof |

---

## 项目文件导航

```
backend/
├── app.py           # 路由 + 启动事件
├── models.py        # ⭐ 数据模型（注意：关系配置）
├── database.py      # ⭐ 支持 SQLite/PostgreSQL 切换
├── services.py      # 业务逻辑
└── requirements.txt # 包含 psycopg2

frontend/
├── src/components/
│   ├── PolicySearch.vue
│   ├── PolicyDetail.vue
│   ├── VersionManage.vue
│   └── StatsView.vue
└── services/api.js  # API 调用

add_policy_cli.py    # ⭐ 政策管理工具（核心工具）

文档/
├── PROJECT_SUMMARY.md  # 本项目完整总结
├── PROJECT_GUIDE.md    # 开发指南
├── POLICY_TRACKING.md  # 政策追踪表
└── HANDOFF_GUIDE.md    # 本文件
```

---

## 部署检查清单

### 前端部署 (Netlify)
- [ ] Build command: `cd frontend && npm run build`
- [ ] Publish: `frontend/dist`
- [ ] Environment: `VITE_API_BASE = https://...railway.app/api`
- [ ] Netlify.toml: 无 BOM，正确的 TOML 格式

### 后端部署 (Railway)
- [ ] Connect GitHub 仓库
- [ ] Add PostgreSQL service
- [ ] Environment: `DATABASE_URL = postgresql://...`
- [ ] Startup: 自动检测 uvicorn

### 数据库持久化
- [ ] PostgreSQL 已部署
- [ ] DATABASE_URL 已设置到后端
- [ ] 后端已重新部署

---

## 常见故障排查

| 问题 | 排查 | 解决 |
|------|------|------|
| API 404 | 检查环境变量 | `VITE_API_BASE` 设置 |
| 中文是 ???? | 用 Python 脚本 | `add_policy_cli.py` |
| 数据丢失 | 检查 DATABASE_URL | 确保 PostgreSQL 连接 |
| 启动报错 | 查看 Railway 日志 | 检查 import 和依赖 |

---

## 最重要的 3 个原则

1. **数据 ≠ 代码**
   - 政策是运行时数据，永不硬编码
   - 通过 API 添加，不改代码

2. **API 为中心**
   - 所有操作都通过 API
   - 前后端完全解耦

3. **工具独立**
   - 添加政策用独立 CLI
   - 不影响部署流程

---

## 下一步优化方向

- [ ] Phase 2: WebSocket 实时推送
- [ ] Phase 3: Webhook API + 密钥管理
- [ ] Phase 4: 政策对比分析
- [ ] Phase 5: 前端中文编码修复

---

## 如何继续开发

### 添加新航司
```bash
python add_policy_cli.py
# 交互式输入，不需要改代码
```

### 遇到新卡点
1. 记录完整错误信息
2. 分析根本原因
3. 优先考虑独立工具解决
4. 更新此文档

### 前端修改
- 编辑 `frontend/src/` 下的组件
- `git push` 自动部署到 Netlify

### 后端修改
- 编辑 `backend/` 下的代码
- `git push` 自动部署到 Railway
- **注意**: 不要在启动事件中添加数据

---

## 文档完整性

- ✅ 项目概览
- ✅ 所有 9 个卡点详细分析
- ✅ 解决方案和经验
- ✅ 标准工作流程
- ✅ 快速参考
- ✅ 故障排查
- ✅ 维护指南

---

**最后更新**: 2026-06-08  
**准备好继续开发**: 是  
**适合 AI 接手**: 是
