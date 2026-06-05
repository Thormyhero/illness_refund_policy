<template>
  <div class="policy-search">
    <!-- 搜索面板 -->
    <div class="search-panel">
      <div class="panel-header">
        <h2>快速检索</h2>
      </div>

      <div class="search-inputs">
        <div class="input-group">
          <label>航司</label>
          <select v-model="policyStore.searchAirline" class="select-input">
            <option value="">全部航司</option>
            <option v-for="airline in policyStore.airlines" :key="airline" :value="airline">
              {{ airline }}
            </option>
          </select>
        </div>

        <div class="input-group">
          <label>票台类型</label>
          <select v-model="policyStore.searchTicketDesk" class="select-input">
            <option value="">全部类型</option>
            <option v-for="desk in policyStore.ticketDesks" :key="desk" :value="desk">
              {{ desk }}
            </option>
          </select>
        </div>

        <button @click="policyStore.resetSearch" class="btn-reset">重置</button>
      </div>

      <div class="stats-info">
        <span class="stat-item">总政策: <strong>{{ policyStore.policies.length }}</strong></span>
        <span class="stat-item">搜索结果: <strong>{{ policyStore.filteredPolicies.length }}</strong></span>
      </div>
    </div>

    <!-- 政策列表 -->
    <div class="policies-container">
      <div v-if="policyStore.loading" class="loading">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>

      <div v-else-if="policyStore.filteredPolicies.length === 0" class="empty">
        <p>暂无相关政策</p>
      </div>

      <div v-else class="policies-grid">
        <div
          v-for="(policy, idx) in policyStore.filteredPolicies"
          :key="policy.id"
          class="policy-card"
          :style="{ '--idx': idx }"
          @click="selectPolicy(policy)"
        >
          <div class="card-accent"></div>
          <div class="card-content">
            <div class="card-header">
              <h3 class="policy-name">{{ policy.airline_name }}</h3>
              <span class="policy-code">{{ policy.airline_code }}</span>
            </div>
            <div class="card-body">
              <p class="policy-info"><span class="label">票台:</span> {{ policy.ticket_desk_type }}</p>
              <p class="policy-info"><span class="label">材料:</span> {{ policy.materials.length }} 项</p>
              <p class="policy-info"><span class="label">版本:</span> v{{ policy.current_version_id }}</p>
            </div>
            <div class="card-footer">
              <time class="update-time">{{ formatDate(policy.updated_at) }}</time>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 政策详情面板 -->
    <PolicyDetail v-if="selectedPolicyLocal" :policy="selectedPolicyLocal" @close="selectedPolicyLocal = null" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { usePolicyStore } from '../stores/policyStore'
import PolicyDetail from './PolicyDetail.vue'

const policyStore = usePolicyStore()
const selectedPolicyLocal = ref(null)

const selectPolicy = (policy) => {
  selectedPolicyLocal.value = policy
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.policy-search {
  animation: fadeIn 0.6s ease-out;
}

.search-panel {
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 32px;
  box-shadow: 0 8px 32px rgba(91, 122, 107, 0.08);
}

.panel-header h2 {
  margin: 0 0 24px 0;
  color: var(--color-primary);
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.3px;
}

.search-inputs {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-group label {
  font-weight: 600;
  color: var(--color-primary);
  font-size: 13px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.select-input {
  padding: 10px 14px;
  border: 1px solid var(--glass-border);
  border-radius: 10px;
  background: rgba(254, 253, 251, 0.8);
  color: var(--color-dark);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  min-width: 180px;
  font-family: inherit;
}

.select-input:hover,
.select-input:focus {
  border-color: var(--color-primary);
  background: rgba(254, 253, 251, 1);
  box-shadow: 0 4px 16px rgba(91, 122, 107, 0.12);
  outline: none;
}

.btn-reset {
  align-self: flex-end;
  padding: 10px 20px;
  background: var(--color-accent);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  font-weight: 600;
}

.btn-reset:hover {
  background: #7a6f6c;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 125, 122, 0.2);
}

.stats-info {
  display: flex;
  gap: 24px;
  color: var(--color-accent);
  font-size: 13px;
  padding-top: 16px;
  border-top: 1px solid var(--glass-border);
}

.stat-item strong {
  color: var(--color-primary);
  font-weight: 700;
}

.policies-container {
  position: relative;
  min-height: 200px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(91, 122, 107, 0.15);
  border-top: 3px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading p {
  color: var(--color-accent);
  margin-top: 16px;
  font-size: 14px;
}

.empty {
  text-align: center;
  padding: 80px 20px;
  color: var(--color-accent);
  font-size: 16px;
}

.policies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.policy-card {
  position: relative;
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  animation: cardSlideIn 0.6s ease-out backwards;
  animation-delay: calc(var(--idx) * 0.08s);
}

@keyframes cardSlideIn {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.policy-card:hover {
  transform: translateY(-8px);
  border-color: var(--color-primary);
  box-shadow: 0 16px 48px rgba(91, 122, 107, 0.16);
}

.card-accent {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-secondary));
  transform: scaleX(0);
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.policy-card:hover .card-accent {
  transform: scaleX(1);
}

.card-content {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.policy-name {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-primary);
  margin: 0;
}

.policy-code {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-light));
  color: white;
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.policy-info {
  margin: 0;
  font-size: 13px;
  color: var(--color-accent);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  font-weight: 600;
  color: var(--color-primary);
}

.card-footer {
  padding-top: 12px;
  border-top: 1px solid var(--glass-border);
}

.update-time {
  font-size: 11px;
  color: #bfb9b5;
  font-style: italic;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .search-inputs {
    flex-direction: column;
  }

  .select-input {
    min-width: auto;
    width: 100%;
  }

  .btn-reset {
    align-self: stretch;
  }

  .policies-grid {
    grid-template-columns: 1fr;
  }
}
</style>
