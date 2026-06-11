# 👋 AI 接手指南 - 从这里开始

## 你好！

你正在接手一个**完整可用的病退政策管理系统**。这个文档帮助你快速理解项目状态和继续开发。

---

## ⚡ 30 秒快速起点

### 当前状态
- ✅ 系统正在运行
- ✅ 前端: https://illnessrefund.netlify.app
- ✅ 后端: https://illnessrefundpolicy-production.up.railway.app
- ✅ 数据库: PostgreSQL (持久化)

### 立即可做的事
```bash
# 添加新航司政策（无需改代码、无需重新部署）
python add_policy_cli.py --code "MU" --name "东方航空" --refund "支持"

# 或交互式添加
python add_policy_cli.py
```

### 验证系统
1. 打开前端：https://illnessrefund.netlify.app
2. 搜索航司代码
3. 查看政策详情

---

## 📚 理解项目：阅读顺序

| 文档 | 用途 | 何时阅读 |
|------|------|--------|
| **本文件** | 快速起点 | 现在 |
| **HANDOFF_GUIDE.md** | 所有卡点的快速参考 | 遇到问题时 |
| **PROJECT_SUMMARY.md** | 完整项目文档 | 理解全貌 |
| **PROJECT_GUIDE.md** | 实战操作指南 | 开始新工作前 |
| **POLICY_TRACKING.md** | 进度追踪 | 管理任务时 |

---

## 🎯 最重要的一件事

**用户明确要求的核心原则**：

```
"我需要一个可以持续增添政策而不影响前后端部署的方式"
```

✅ **正确做法**：用 `add_policy_cli.py` 添加数据  
❌ **错误做法**：修改代码、重新部署

这个工具是为了实现**零代码改动的数据管理**而专门设计的。

---

## 🔴 曾经遇到的 9 大卡点

| # | 问题 | 原因 | 解决 |
|---|------|------|------|
| 1 | netlify.toml 无法解析 | UTF-8 BOM | 删除 BOM |
| 2 | API 404 错误 | 环境变量未设置 | 设置 VITE_API_BASE |
| 3 | Vue 编译错误 | 重复的模板块 | 删除重复 |
| 4 | SQLAlchemy 报错 | 循环外键 | 移除 ForeignKey，添加 foreign_keys 参数 |
| 5 | 字段溢出 | String(10) 太短 | 改为 String(100) |
| 6 | 数据丢失 | SQLite 在内存 | 配置 PostgreSQL |
| 7 | ImportError | init_db 缺失 | 添加回函数 |
| 8 | 中文是 ???? | PowerShell 编码 | 用 Python 脚本 |
| 9 | 每次改数据都要部署 | 数据硬编码在代码 | 独立 CLI 工具 |

**详细分析** → 见 HANDOFF_GUIDE.md

---

## 📁 项目文件导航

```
illness_refund_policy/
├── backend/                    # FastAPI 后端
│   ├── app.py                 # 主应用
│   ├── models.py              # ⭐ 数据模型
│   ├── database.py            # ⭐ 数据库配置
│   └── requirements.txt
│
├── frontend/                   # Vue3 前端
│   ├── src/components/        # 4 个核心组件
│   ├── netlify.toml          # ⭐ 部署配置（BOM 已移除）
│   └── vite.config.js         # ⭐ API 代理配置
│
├── add_policy_cli.py           # ⭐ 核心工具（添加政策）
├── PROJECT_SUMMARY.md          # 完整项目文档
├── HANDOFF_GUIDE.md            # 快速参考（卡点汇总）
├── PROJECT_GUIDE.md            # 实战指南
├── POLICY_TRACKING.md          # 进度追踪
└── AI_HANDOFF_README.md        # 本文件
```

**关键文件标记 ⭐**：修改这些文件时特别小心。

---

## 🚀 常见工作流程

### 添加新政策
```bash
python add_policy_cli.py

# 按提示输入：
# 1. 航司代码 (如 "MU")
# 2. 航司名称 (如 "东方航空")
# 3. 可申请性等

# 不需要改代码，不需要重新部署！
```

### 修改前端
```bash
cd frontend
# 编辑 src/components 下的文件
git push  # 自动部署到 Netlify
```

### 修改后端
```bash
cd backend
# 编辑 app.py, models.py 等
git push  # 自动部署到 Railway
```

---

## 🆘 遇到问题

### 前端显示 404
**排查**：
1. 检查 Netlify 环境变量 `VITE_API_BASE` 是否设置
2. 检查是否含有完整的后端 URL

### 后端启动失败
**排查**：
1. 查看 Railway 日志
2. 检查 DATABASE_URL 环境变量
3. 检查 requirements.txt 是否包含 psycopg2-binary

### 数据添加后看不到
**排查**：
1. 前端按 Ctrl+Shift+R 清除缓存
2. 确认 add_policy_cli.py 返回 200 状态
3. 检查前端搜索条件是否正确

**详细故障排查** → 见 HANDOFF_GUIDE.md

---

## 📊 系统架构（一句话）

```
Vue3 前端 (Netlify)
    ↓ HTTP/API
FastAPI 后端 (Railway)
    ↓ 数据库连接
PostgreSQL (持久化存储)
```

独立工具 `add_policy_cli.py` → API → 数据库

---

## ✅ 验证清单：系统健康检查

每次接手后，立即检查：

- [ ] 打开 https://illnessrefund.netlify.app，页面加载成功
- [ ] 在搜索框输入 "FD"，能搜到亚航集团政策
- [ ] 点击政策，能看到 6 种材料要求
- [ ] 点击"版本管理"，能看到版本历史
- [ ] 运行 `python add_policy_cli.py --code "TEST" --name "测试航空"`，成功添加
- [ ] 刷新前端，新政策出现在列表中

如果以上都能通过，系统健康！👍

---

## 🎯 下一步优化（Phase 2-4）

### Phase 2：WebSocket 实时推送
- **目标**：前端不用手动刷新，自动看到新政策
- **代码示例**：见 PROJECT_GUIDE.md 第 184-282 行

### Phase 3：Webhook API
- **目标**：外部 AI 系统可通过 HTTP 调用更新政策
- **代码示例**：见 PROJECT_GUIDE.md 第 286-358 行

### Phase 4+：高级功能
- 政策对比分析
- 批量导入/导出
- AI 自动拆解辅助

---

## 📞 关键概念速记

| 概念 | 含义 | 重要性 |
|------|------|--------|
| **add_policy_cli.py** | 独立的政策管理工具 | 🔴 极高 |
| **API 为中心** | 所有操作都通过 API，不改代码 | 🔴 极高 |
| **PostgreSQL 持久化** | 数据不会在重启后丢失 | 🟠 高 |
| **环境变量配置** | 不把敏感信息写在代码 | 🟠 高 |
| **版本管理** | 每次修改自动创建新版本 | 🟡 中 |

---

## 🔗 重要链接

- **前端**: https://illnessrefund.netlify.app
- **后端 API 文档**: https://illnessrefundpolicy-production.up.railway.app/docs
- **GitHub**: https://github.com/Thormyhero/illness_refund_policy
- **Railway 仪表板**: https://railway.app (你需要访问权限)
- **Netlify 仪表板**: https://netlify.com (你需要访问权限)

---

## 💡 最后的话

这个项目体现了**正确的架构设计**：

✅ **数据与代码分离** - 核心原则  
✅ **API 为中心** - 前后端解耦  
✅ **独立工具** - 数据管理不影响部署  
✅ **文档完善** - 易于维护和交接  

祝你开发顺利！如果有问题，从 HANDOFF_GUIDE.md 开始查找。

---

**最后更新**: 2026-06-08  
**维护者**: 初始化 AI  
**下一个维护者**: 你！👋
