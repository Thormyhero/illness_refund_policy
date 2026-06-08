<template>
  <div class="version-manage">
    <div class="manage-panel">
      <div class="panel-header">
        <h2>版本时间线</h2>
        <p>选择政策查看历史版本和回滚选项</p>
      </div>

      <div class="policy-selector">
        <label>选择政策</label>
        <select v-model="selectedPolicyId" class="select-input">
          <option value="">-- 选择政策 --</option>
          <option v-for="policy in policyStore.policies" :key="policy.id" :value="policy.id">
            {{ policy.airline_name }} ({{ policy.airline_code }})
          </option>
        </select>
      </div>
    </div>

    <!-- 版本时间线 -->
    <div v-if="selectedPolicyId && policyStore.currentVersions.length > 0" class="timeline-container">
      <div class="timeline">
        <div
          v-for="(version, index) in policyStore.currentVersions"
          :key="version.id"
          class="timeline-item"
          :class="{ 'is-current': index === 0 }"
        >
          <div class="timeline-marker" :class="version.operation_type"></div>

          <div class="timeline-content">
            <div class="version-header">
              <span class="version-tag">{{ version.version_tag }}</span>
              <span class="operation-badge" :class="version.operation_type">
                {{ getOperationLabel(version.operation_type) }}
              </span>
            </div>

            <div class="version-meta">
              <p><span class="meta-label">操作者:</span> {{ version.operator }}</p>
              <p><span class="meta-label">时间:</span> {{ formatDate(version.created_at) }}</p>
            </div>

            <p v-if="version.changes_summary" class="version-summary">
              {{ version.changes_summary }}
            </p>

            <div class="version-actions">
              <button v-if="index > 0" class="btn-rollback" @click="handleRollback(version)">
                回滚到此版本
              </button>
              <button class="btn-detail" @click="toggleDetail(version.id)">
                查看详情
              </button>
            </div>

            <!-- 变更详情 -->
            <div v-if="expandedVersion === version.id && version.changes_detail" class="change-detail">
              <pre>{{ JSON.stringify(version.changes_detail, null, 2) }}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <p>请选择一个政策以查看版本历史</p>
    </div>

    <!-- 回滚确认对话框 -->
    <RollbackConfirm
      v-if="rollbackConfirm.show"
      :current-version="rollbackConfirm.currentVersion"
      :target-version="rollbackConfirm.targetVersion"
      :policy-id="parseInt(selectedPolicyId)"
      @confirm="confirmRollback"
      @cancel="rollbackConfirm.show = false"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { usePolicyStore } from '../stores/policyStore'
import RollbackConfirm from './RollbackConfirm.vue'

const policyStore = usePolicyStore()
const selectedPolicyId = ref('')
const expandedVersion = ref(null)

const rollbackConfirm = ref({
  show: false,
  currentVersion: null,
  targetVersion: null,
})

watch(selectedPolicyId, async (newId) => {
  if (newId) {
    await policyStore.fetchVersions(newId)
    await policyStore.fetchAuditLogs(newId)
  }
})

const getOperationLabel = (type) => {
  const labels = {
    create: '✨ 创建',
    update: '✏️ 更新',
    rollback: '🔄 回滚',
  }
  return labels[type] || type
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}

const toggleDetail = (versionId) => {
  expandedVersion.value = expandedVersion.value === versionId ? null : versionId
}

const handleRollback = (targetVersion) => {
  const currentVersion = policyStore.currentVersions[0]
  rollbackConfirm.value = {
    show: true,
    currentVersion,
    targetVersion,
  }
}

const confirmRollback = async (operator) => {
  try {
    await policyStore.rollbackToVersion(
      parseInt(selectedPolicyId.value),
      rollbackConfirm.value.targetVersion.id,
      operator
    )
    rollbackConfirm.value.show = false
    alert('✓ 回滚成功！')
  } catch (err) {
    alert(`✗ 回滚失败: ${err.message}`)
  }
}
</script>

<style scoped>
.version-manage {
  animation: fadeIn 0.6s ease-out;
}

.manage-panel {
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 32px;
  box-shadow: 0 8px 32px rgba(91, 122, 107, 0.08);
}

.panel-header {
  margin-bottom: 24px;
}

.panel-header h2 {
  margin: 0 0 8px 0;
  color: var(--color-primary);
  font-size: 18px;
  font-weight: 700;
}

.panel-header p {
  margin: 0;
  color: var(--color-accent);
  font-size: 13px;
}

.policy-selector {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.policy-selector label {
  font-weight: 600;
  color: var(--color-primary);
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.select-input {
  padding: 12px 14px;
  border: 1px solid var(--glass-border);
  border-radius: 10px;
  background: rgba(254, 253, 251, 0.9);
  color: var(--color-dark);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  font-family: inherit;
}

.select-input:hover,
.select-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 4px 16px rgba(91, 122, 107, 0.12);
  outline: none;
}

.timeline-container {
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 8px 32px rgba(91, 122, 107, 0.08);
}

.timeline {
  position: relative;
  padding-left: 30px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, var(--color-primary), var(--color-secondary));
}

.timeline-item {
  position: relative;
  margin-bottom: 28px;
  padding-bottom: 28px;
  animation: slideIn 0.5s ease-out backwards;
}

.timeline-item:nth-child(n) {
  animation-delay: calc(var(--idx, 0) * 0.08s);
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.timeline-marker {
  position: absolute;
  left: -36px;
  top: 0;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--color-primary);
  border: 3px solid white;
  box-shadow: 0 0 0 2px var(--color-primary);
  transition: all 0.3s ease;
}

.timeline-marker.create {
  background: #7a9684;
  box-shadow: 0 0 0 2px #7a9684;
}

.timeline-marker.update {
  background: var(--color-secondary);
  box-shadow: 0 0 0 2px var(--color-secondary);
}

.timeline-marker.rollback {
  background: var(--color-accent);
  box-shadow: 0 0 0 2px var(--color-accent);
}

.timeline-item.is-current .timeline-marker {
  width: 16px;
  height: 16px;
  left: -38px;
}

.timeline-content {
  background: rgba(254, 253, 251, 0.6);
  padding: 16px;
  border-radius: 8px;
  border-left: 3px solid var(--color-primary);
}

.timeline-item.is-current .timeline-content {
  background: rgba(254, 253, 251, 0.9);
  box-shadow: 0 2px 12px rgba(91, 122, 107, 0.08);
}

.version-header {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
  align-items: center;
}

.version-tag {
  font-weight: 700;
  color: var(--color-primary);
  font-size: 13px;
  font-family: 'Courier New', monospace;
}

.operation-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  background: rgba(91, 122, 107, 0.1);
  color: var(--color-primary);
}

.operation-badge.update {
  background: rgba(196, 165, 160, 0.1);
  color: var(--color-secondary);
}

.operation-badge.rollback {
  background: rgba(139, 125, 122, 0.1);
  color: var(--color-accent);
}

.version-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 12px;
}

.version-meta p {
  margin: 0;
  font-size: 12px;
  color: var(--color-accent);
}

.meta-label {
  font-weight: 600;
  color: var(--color-primary);
}

.version-summary {
  margin: 12px 0;
  padding: 12px;
  background: rgba(91, 122, 107, 0.05);
  border-radius: 6px;
  font-size: 13px;
  color: var(--color-dark);
  border-left: 2px solid var(--color-primary);
}

.version-actions {
  display: flex;
  gap: 12px;
  margin-top: 12px;
  flex-wrap: wrap;
}

.btn-rollback,
.btn-detail {
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-rollback {
  background: var(--color-secondary);
  color: white;
}

.btn-rollback:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(196, 165, 160, 0.3);
}

.btn-detail {
  background: var(--color-primary);
  color: white;
}

.btn-detail:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(91, 122, 107, 0.3);
}

.change-detail {
  margin-top: 12px;
}

.change-detail pre {
  background: rgba(91, 122, 107, 0.05);
  padding: 12px;
  border-radius: 6px;
  font-size: 11px;
  color: var(--color-dark);
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  margin: 0;
}

.empty-state {
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: 80px 20px;
  text-align: center;
  color: var(--color-accent);
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
  .version-actions {
    flex-direction: column;
  }

  .btn-rollback,
  .btn-detail {
    width: 100%;
  }
}
</style>
