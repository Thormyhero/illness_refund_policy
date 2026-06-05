import axios from 'axios'

// 获取 API 基础地址
// 开发环境：http://localhost:8000
// 生产环境（Railway）：相对路径 /api（由后端统一服务）
const API_BASE_URL = import.meta.env.VITE_API_BASE || '/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 政策 API
export const policyAPI = {
  // 创建政策
  create(data) {
    return apiClient.post('/policies', data)
  },

  // 获取政策列表
  list(airlineCode = null, ticketDeskType = null) {
    const params = {}
    if (airlineCode) params.airline_code = airlineCode
    if (ticketDeskType) params.ticket_desk_type = ticketDeskType
    return apiClient.get('/policies', { params })
  },

  // 获取单个政策
  get(id) {
    return apiClient.get(`/policies/${id}`)
  },

  // 更新政策
  update(id, data, operator = 'manual') {
    return apiClient.put(`/policies/${id}?operator=${operator}`, data)
  },

  // 删除政策
  delete(id) {
    return apiClient.delete(`/policies/${id}`)
  },
}

// 材料 API
export const materialAPI = {
  // 添加材料
  create(policyId, data) {
    return apiClient.post(`/policies/${policyId}/materials`, data)
  },

  // 获取材料列表
  list(policyId) {
    return apiClient.get(`/policies/${policyId}/materials`)
  },

  // 更新材料
  update(id, data) {
    return apiClient.put(`/materials/${id}`, data)
  },

  // 删除材料
  delete(id) {
    return apiClient.delete(`/materials/${id}`)
  },
}

// 版本 API
export const versionAPI = {
  // 获取版本列表
  list(policyId) {
    return apiClient.get(`/policies/${policyId}/versions`)
  },

  // 获取单个版本
  get(id) {
    return apiClient.get(`/versions/${id}`)
  },

  // 回滚到指定版本
  rollback(policyId, versionId, operator = 'manual') {
    return apiClient.post(`/policies/${policyId}/versions/${versionId}/rollback?operator=${operator}`)
  },
}

// 审计日志 API
export const auditAPI = {
  // 获取审计日志
  list(policyId) {
    return apiClient.get(`/policies/${policyId}/audit-logs`)
  },
}

// 统计 API
export const statsAPI = {
  // 获取统计信息
  get() {
    return apiClient.get('/stats')
  },
}

// 健康检查
export const healthAPI = {
  check() {
    return axios.get('/health')
  },
}
