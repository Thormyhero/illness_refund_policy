import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { policyAPI, versionAPI, auditAPI, statsAPI } from '../services/api'

export const usePolicyStore = defineStore('policy', () => {
  // State
  const policies = ref([])
  const selectedPolicy = ref(null)
  const currentVersions = ref([])
  const currentAuditLogs = ref([])
  const stats = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // 搜索条件
  const searchAirline = ref('')
  const searchTicketDesk = ref('')

  // Getters
  const filteredPolicies = computed(() => {
    return policies.value.filter(p => {
      if (searchAirline.value && p.airline_code !== searchAirline.value) return false
      if (searchTicketDesk.value && p.ticket_desk_type !== searchTicketDesk.value) return false
      return true
    })
  })

  const airlines = computed(() => {
    const set = new Set(policies.value.map(p => p.airline_code))
    return Array.from(set).sort()
  })

  const ticketDesks = computed(() => {
    const set = new Set(policies.value.map(p => p.ticket_desk_type))
    return Array.from(set).sort()
  })

  // Actions
  const fetchPolicies = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await policyAPI.list()
      policies.value = response.data
    } catch (err) {
      error.value = err.message
      console.error('Failed to fetch policies:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchPolicy = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await policyAPI.get(id)
      selectedPolicy.value = response.data

      // 同时获取版本历史和审计日志
      await Promise.all([fetchVersions(id), fetchAuditLogs(id)])
    } catch (err) {
      error.value = err.message
      console.error('Failed to fetch policy:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchVersions = async (policyId) => {
    try {
      const response = await versionAPI.list(policyId)
      currentVersions.value = response.data
    } catch (err) {
      console.error('Failed to fetch versions:', err)
    }
  }

  const fetchAuditLogs = async (policyId) => {
    try {
      const response = await auditAPI.list(policyId)
      currentAuditLogs.value = response.data
    } catch (err) {
      console.error('Failed to fetch audit logs:', err)
    }
  }

  const fetchStats = async () => {
    try {
      const response = await statsAPI.get()
      stats.value = response.data
    } catch (err) {
      console.error('Failed to fetch stats:', err)
    }
  }

  const updatePolicy = async (id, data, operator = 'manual') => {
    loading.value = true
    error.value = null
    try {
      const response = await policyAPI.update(id, data, operator)
      selectedPolicy.value = response.data
      await fetchPolicies()
      await fetchVersions(id)
      await fetchAuditLogs(id)
    } catch (err) {
      error.value = err.message
      console.error('Failed to update policy:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const rollbackToVersion = async (policyId, versionId, operator = 'manual') => {
    loading.value = true
    error.value = null
    try {
      const response = await versionAPI.rollback(policyId, versionId, operator)
      selectedPolicy.value = response.data
      await fetchVersions(policyId)
      await fetchAuditLogs(policyId)
      await fetchPolicies()
    } catch (err) {
      error.value = err.message
      console.error('Failed to rollback:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const resetSearch = () => {
    searchAirline.value = ''
    searchTicketDesk.value = ''
  }

  return {
    // State
    policies,
    selectedPolicy,
    currentVersions,
    currentAuditLogs,
    stats,
    loading,
    error,
    searchAirline,
    searchTicketDesk,

    // Getters
    filteredPolicies,
    airlines,
    ticketDesks,

    // Actions
    fetchPolicies,
    fetchPolicy,
    fetchVersions,
    fetchAuditLogs,
    fetchStats,
    updatePolicy,
    rollbackToVersion,
    resetSearch,
  }
})
