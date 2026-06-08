# 🎯 病退政策管理系统 - 完整工作指南

## 📊 项目现状

### ✅ 已完成
- [x] 后端 FastAPI 服务（Railway 部署）
- [x] 前端 Vue 3 应用（Netlify 部署）
- [x] 基础 CRUD API
- [x] 版本管理和回滚机制
- [x] 审计日志系统
- [x] API 与前端连接成功
- [x] 亚航集团示例数据添加

### 🔧 当前阶段
**验证前端功能并继续添加政策数据** ← 你在这里

---

## 📝 政策拆解标准流程（4步法）

根据亚航集团案例，标准的拆解流程：

### **第 1 步：按票台类型分类**
- 检查政策是否有不同票台的差异
- 如果一致，标记为 `ticket_desk_type: "all"`

### **第 2 步：判断可申请性**
```json
"applicability": {
  "refund": "支持 | 否 | 支持(条件)",
  "rebooking": "支持 | 否 | 支持(条件)"
}
```

### **第 3 步：提取时间限制**
```json
"time_limits": {
  "cancel_seat": true,              // 必须在起飞前提出
  "advance_hours": "起飞前/数字",   // 提前多少小时
  "material_deadline": "客票有效期内" // 材料最晚提交时限
}
```

### **第 4 步：逐行拆解材料要求**

| 材料类型 | 代码 | 说明 |
|--------|------|------|
| 购票证件 | `ticketing_document` | 用于证明乘客身份 |
| 诊断证明 | `medical_certificate` | 医生开具的不适宜乘机证明 |
| 住院证明 | `hospital_records` | 出院小结 |
| 检查报告 | `inspection_report` | 化验/MRI/CT/X-光等 |
| 医疗发票 | `medical_invoice` | 缴费证明 |
| 陪同人证明 | `companion_proof` | 直系亲属关系证明 |

每种材料需要填写：
- **定义**：完整的描述（从原文复制/重写）
- **简要规则**：3-5 条核心要点（数组格式）

---

## 🚀 实战：如何添加新政策

### 方案 1：使用快速脚本（推荐）

1. **获取脚本**：
```bash
# 已提供：add_policy.sh
```

2. **修改配置**（编辑脚本中的变量）：
```bash
AIRLINE_CODE="MU"
AIRLINE_NAME="中国东方航空"
TICKET_DESK_TYPE="all"
REFUND_SUPPORT="支持"
REBOOKING_SUPPORT="否"
...
```

3. **运行**：
```bash
bash add_policy.sh
```

### 方案 2：用 curl 直接调用

```bash
curl -X POST "https://illnessrefundpolicy-production.up.railway.app/api/policies" \
  -H "Content-Type: application/json" \
  -d '{
    "airline_code": "MU",
    "airline_name": "中国东方航空",
    "ticket_desk_type": "all",
    "raw_policy": "政策原文...",
    "breakdown_json": {
      "applicability": {"refund": "支持", "rebooking": "否"},
      "time_limits": {"cancel_seat": true, "advance_hours": 4}
    }
  }'
```

---

## ✅ 验证清单

### 前端功能验证
- [ ] 刷新 https://illnessrefund.netlify.app
- [ ] 在"航司"下拉框搜索 "FD"
- [ ] 显示"亚航集团"政策
- [ ] 显示 6 种材料要求
- [ ] 原文可点击隐藏/展示
- [ ] 能查看版本历史
- [ ] 能编辑和回滚版本

### 数据准确性
- [ ] 所有材料的定义完整
- [ ] 简要规则清晰准确
- [ ] 时间限制正确标记
- [ ] 可申请性标记准确

---

## 🔄 Phase 2：实时更新（WebSocket）

### 当前问题
前端需要**手动刷新**才能看到新政策。

### 解决方案
实现 WebSocket `/ws/policies` 端点，当政策更新时自动推送给所有连接的前端。

### 实现步骤
1. 后端添加 WebSocket 路由
2. 创建连接管理器
3. 政策更新时广播消息
4. 前端连接 WebSocket 并监听更新

---

## 🔑 Phase 3：Webhook API

### 目标
让外部 AI 系统能通过 HTTP 调用更新政策。

### 关键功能
- 生成和管理 API Key
- Webhook 端点验证
- 外部系统调用更新

### 使用示例
```bash
curl -X POST "https://.../api/webhooks/update-policy" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "policy_id": 1,
    "raw_policy": "更新的政策...",
    "breakdown_json": {...}
  }'
```

---

## 📋 进度追踪

| 阶段 | 任务 | 状态 |
|------|------|------|
| Phase 1 | 添加 FD 航司 | ✅ 完成 |
| Phase 1 | 验证前端显示 | 🔄 进行中 |
| Phase 1 | 再添加 3-5 个航司 | ⏳ 待做 |
| Phase 2 | WebSocket 实时推送 | ⏳ 待做 |
| Phase 3 | Webhook API | ⏳ 待做 |

---

## 🎯 现在立即做

1. **验证前端**
   - 打开 https://illnessrefund.netlify.app
   - 搜索航司代码 "FD"
   - 检查政策是否显示

2. **告诉我结果**
   - 能看到政策吗？
   - 6 种材料都显示了吗？
   - 有什么显示不对的地方吗？

3. **继续添加下一个航司**
   - 提供新航司的政策原文
   - 我帮你拆解并添加

---

## 📞 常见问题

**Q: 如何快速批量添加多个航司？**
A: 可以创建批量脚本，逐行读取 CSV 并自动添加。

**Q: 政策有多个票台类型的差异怎么办？**
A: 为每个不同的票台类型创建独立的政策记录。

**Q: 如何修改已添加的政策？**
A: 在前端点击"编辑"，修改后会自动创建新版本，旧版本可回滚。

**Q: 能导入 Excel 吗？**
A: 可以，我们可以创建一个导入脚本。

---

**现在验证前端，告诉我结果！** 🚀
