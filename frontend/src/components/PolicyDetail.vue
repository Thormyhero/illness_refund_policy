<template>
  <div class="detail-modal-overlay" @click.self="$emit('close')">
    <div class="detail-modal">
      <!-- 头部 -->
      <div class="modal-header">
        <div class="header-info">
          <h2>{{ policy.airline_name }}</h2>
          <span class="badge">{{ policy.airline_code }} • {{ policy.ticket_desk_type }}</span>
        </div>
        <button class="btn-close" @click="$emit('close')">✕</button>
      </div>

      <!-- 内容区域 -->
      <div class="modal-content">
        <!-- 原文部分 -->
        <section class="section">
          <div class="section-header" @click="showRaw = !showRaw">
            <h3>政策原文</h3>
            <span class="toggle-icon">{{ showRaw ? '▼' : '▶' }}</span>
          </div>
          <div v-show="showRaw" class="raw-policy">
            <p>{{ policy.raw_policy || '暂无原文内容' }}</p>
          </div>
        </section>

        <!-- 拆解结果 -->
        <section class="section">
          <h3>拆解结果</h3>

          <!-- 可申请性 -->
          <div v-if="policy.breakdown?.applicability" class="subsection">
            <h4>可申请性</h4>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">因病退票:</span>
                <span class="value">{{ policy.breakdown.applicability.refund || 'N/A' }}</span>
              </div>
              <div class="info-item">
                <span class="label">因病改期:</span>
                <span class="value">{{ policy.breakdown.applicability.rebooking || 'N/A' }}</span>
              </div>
            </div>
          </div>

          <!-- 操作时限 -->
          <div v-if="policy.breakdown?.time_limits" class="subsection">
            <h4>操作时限</h4>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">需要取消机位:</span>
                <span class="value">{{ policy.breakdown.time_limits.cancel_seat ? '是' : '否' }}</span>
              </div>
              <div class="info-item">
                <span class="label">提前取消时间:</span>
                <span class="value">{{ policy.breakdown.time_limits.advance_hours || 'N/A' }}</span>
              </div>
            </div>
          </div>

          <!-- 材料要求 -->
          <div v-if="policy.materials.length > 0" class="subsection">
            <h4>材料要求 ({{ policy.materials.length }}项)</h4>
            <div class="materials-list">
              <div
                v-for="material in policy.materials"
                :key="material.id"
                class="material-item"
                @click="toggleMaterialDetail(material.id)"
              >
                <div class="material-header">
                  <span class="material-type">{{ getMaterialLabel(material.material_type) }}</span>
                  <span class="toggle-icon">{{ expandedMaterial === material.id ? '▼' : '▶' }}</span>
                </div>

                <div v-show="expandedMaterial === material.id" class="material-detail">
                  <div class="definition">
                    <p class="label-text">完整定义:</p>
                    <p class="content-text">{{ material.definition }}</p>
                  </div>

                  <div v-if="material.simple_rules.length > 0" class="rules">
                    <p class="label-text">简要规则:</p>
                    <ul>
                      <li v-for="(rule, idx) in material.simple_rules" :key="idx" class="rule-item">
                        {{ rule }}
                      </li>
                    </ul>
                  </div>

                  <button class="btn-copy" @click.stop="copyToClipboard(material)">
                    复制规则
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 版本信息 -->
        <section class="section">
          <h4>版本信息</h4>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">当前版本:</span>
              <span class="value">v{{ policy.current_version_id }}</span>
            </div>
            <div class="info-item">
              <span class="label">创建时间:</span>
              <span class="value">{{ formatDate(policy.created_at) }}</span>
            </div>
            <div class="info-item">
              <span class="label">最后更新:</span>
              <span class="value">{{ formatDate(policy.updated_at) }}</span>
            </div>
          </div>
        </section>
      </div>

      <!-- 底部操作 -->
      <div class="modal-footer">
        <button class="btn-primary" @click="handleExport">导出 JSON</button>
        <button class="btn-secondary" @click="handleVersionHistory">版本历史</button>
        <button class="btn-close-modal" @click="$emit('close')">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  policy: {
    type: Object,
    required: true,
  },
})

defineEmits(['close'])

const showRaw = ref(false)
const expandedMaterial = ref(null)

const toggleMaterialDetail = (materialId) => {
  expandedMaterial.value = expandedMaterial.value === materialId ? null : materialId
}

const getMaterialLabel = (type) => {
  const labels = {
    ticketing_document: '证件要求',
    medical_certificate: '诊断证明',
    hospital_records: '住院证明',
    inspection_report: '检查报告',
    medical_invoice: '医疗发票',
    companion_proof: '陪同人证明',
  }
  return labels[type] || type
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}

const copyToClipboard = (material) => {
  const text = `${getMaterialLabel(material.material_type)}\n\n定义:\n${material.definition}\n\n规则:\n${material.simple_rules.map(r => `• ${r}`).join('\n')}`
  navigator.clipboard.writeText(text)
  alert('✓ 已复制到剪贴板')
}

const handleExport = () => {
  const dataStr = JSON.stringify(props.policy, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${props.policy.airline_code}-policy.json`
  link.click()
  URL.revokeObjectURL(url)
}

const handleVersionHistory = () => {
  alert('版本历史功能 - 将在版本管理页面中详细展示')
}
</script>

<style scoped>
.detail-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(61, 61, 61, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  animation: fadeIn 0.3s ease-out;
  backdrop-filter: blur(4px);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.detail-modal {
  background: var(--color-card);
  border-radius: 16px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(91, 122, 107, 0.15);
  animation: slideUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid rgba(91, 122, 107, 0.1);
}

.header-info h2 {
  margin: 0;
  font-size: 18px;
  color: var(--color-primary);
  margin-bottom: 8px;
  font-weight: 700;
}

.badge {
  display: inline-block;
  background: rgba(91, 122, 107, 0.1);
  color: var(--color-primary);
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--color-accent);
  transition: color 0.3s ease;
}

.btn-close:hover {
  color: var(--color-primary);
}

.modal-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.section {
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: rgba(91, 122, 107, 0.05);
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.section-header:hover {
  background: rgba(91, 122, 107, 0.08);
}

.section-header h3 {
  margin: 0;
  font-size: 14px;
  color: var(--color-primary);
  font-weight: 700;
}

.toggle-icon {
  color: var(--color-secondary);
  font-size: 12px;
}

.section h3 {
  margin: 0 0 16px 0;
  font-size: 14px;
  color: var(--color-primary);
  font-weight: 700;
}

.section h4 {
  margin: 0 0 12px 0;
  font-size: 13px;
  color: var(--color-primary);
  font-weight: 700;
}

.raw-policy {
  background: rgba(245, 243, 240, 0.5);
  border: 1px solid rgba(91, 122, 107, 0.1);
  border-radius: 8px;
  padding: 16px;
  margin-top: 12px;
  max-height: 200px;
  overflow-y: auto;
  white-space: pre-wrap;
  font-size: 12px;
  color: var(--color-accent);
  line-height: 1.6;
}

.subsection {
  margin: 16px 0;
  padding: 16px;
  background: rgba(245, 243, 240, 0.3);
  border-radius: 8px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 8px;
  background: white;
  border-radius: 6px;
  border: 1px solid rgba(91, 122, 107, 0.05);
}

.label {
  font-weight: 700;
  color: var(--color-primary);
  font-size: 12px;
}

.value {
  color: var(--color-dark);
  font-weight: 600;
  font-size: 12px;
}

.materials-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.material-item {
  border: 1px solid rgba(91, 122, 107, 0.1);
  border-radius: 8px;
  overflow: hidden;
  background: rgba(245, 243, 240, 0.3);
}

.material-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.material-header:hover {
  background: rgba(91, 122, 107, 0.05);
}

.material-type {
  font-weight: 700;
  color: var(--color-primary);
  font-size: 13px;
}

.material-detail {
  padding: 16px;
  border-top: 1px solid rgba(91, 122, 107, 0.1);
  background: white;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.definition,
.rules {
  margin-bottom: 12px;
}

.label-text {
  font-weight: 700;
  color: var(--color-primary);
  margin: 0 0 8px 0;
  font-size: 12px;
}

.content-text {
  margin: 0;
  color: var(--color-dark);
  font-size: 12px;
  line-height: 1.6;
}

.rules ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.rule-item {
  padding: 6px 0;
  color: var(--color-accent);
  font-size: 12px;
  line-height: 1.5;
}

.rule-item:before {
  content: '• ';
  color: var(--color-secondary);
  font-weight: bold;
  margin-right: 8px;
}

.btn-copy {
  margin-top: 12px;
  padding: 8px 16px;
  background: var(--color-secondary);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-copy:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(196, 165, 160, 0.3);
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid rgba(91, 122, 107, 0.1);
  background: rgba(245, 243, 240, 0.3);
}

.btn-primary,
.btn-secondary,
.btn-close-modal {
  flex: 1;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(91, 122, 107, 0.2);
}

.btn-secondary {
  background: rgba(91, 122, 107, 0.1);
  color: var(--color-primary);
  border: 1px solid rgba(91, 122, 107, 0.2);
}

.btn-secondary:hover {
  background: rgba(91, 122, 107, 0.15);
}

.btn-close-modal {
  background: rgba(91, 122, 107, 0.1);
  color: var(--color-primary);
  border: 1px solid rgba(91, 122, 107, 0.2);
}

.btn-close-modal:hover {
  background: rgba(91, 122, 107, 0.15);
}

@media (max-width: 768px) {
  .detail-modal {
    max-height: none;
    border-radius: 12px 12px 0 0;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .modal-footer {
    flex-wrap: wrap;
  }

  .btn-primary,
  .btn-secondary,
  .btn-close-modal {
    min-width: 100%;
  }
}
</style>
    <div class="detail-modal">
      <!-- 头部 -->
      <div class="modal-header">
        <div class="header-info">
          <h2>{{ policy.airline_name }} ({{ policy.airline_code }})</h2>
          <span class="badge">{{ policy.ticket_desk_type }}</span>
        </div>
        <button class="btn-close" @click="$emit('close')">✕</button>
      </div>

      <!-- 内容区域 -->
      <div class="modal-content">
        <!-- 原文部分 -->
        <section class="section">
          <div class="section-header" @click="showRaw = !showRaw">
            <h3>📄 原文政策</h3>
            <span class="toggle-icon">{{ showRaw ? '▼' : '▶' }}</span>
          </div>
          <div v-show="showRaw" class="raw-policy">
            <p>{{ policy.raw_policy || '暂无原文内容' }}</p>
          </div>
        </section>

        <!-- 拆解结果 -->
        <section class="section">
          <h3>📋 拆解结果</h3>

          <!-- 可申请性 -->
          <div v-if="policy.breakdown?.applicability" class="subsection">
            <h4>✓ 可申请性</h4>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">因病退票:</span>
                <span class="value">{{ policy.breakdown.applicability.refund || 'N/A' }}</span>
              </div>
              <div class="info-item">
                <span class="label">因病改期:</span>
                <span class="value">{{ policy.breakdown.applicability.rebooking || 'N/A' }}</span>
              </div>
            </div>
          </div>

          <!-- 操作时限 -->
          <div v-if="policy.breakdown?.time_limits" class="subsection">
            <h4>⏱️ 操作时限</h4>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">需要取消机位:</span>
                <span class="value">{{ policy.breakdown.time_limits.cancel_seat ? '是' : '否' }}</span>
              </div>
              <div class="info-item">
                <span class="label">提前取消时间:</span>
                <span class="value">{{ policy.breakdown.time_limits.advance_hours || 'N/A' }}</span>
              </div>
            </div>
          </div>

          <!-- 材料要求 -->
          <div v-if="policy.materials.length > 0" class="subsection">
            <h4>📋 材料要求 ({{ policy.materials.length }}项)</h4>
            <div class="materials-list">
              <div
                v-for="material in policy.materials"
                :key="material.id"
                class="material-item"
                @click="toggleMaterialDetail(material.id)"
              >
                <div class="material-header">
                  <span class="material-type">{{ getMaterialLabel(material.material_type) }}</span>
                  <span class="toggle-icon">{{ expandedMaterial === material.id ? '▼' : '▶' }}</span>
                </div>

                <div v-show="expandedMaterial === material.id" class="material-detail">
                  <div class="definition">
                    <p class="label-text">完整定义:</p>
                    <p class="content-text">{{ material.definition }}</p>
                  </div>

                  <div v-if="material.simple_rules.length > 0" class="rules">
                    <p class="label-text">简要规则:</p>
                    <ul>
                      <li v-for="(rule, idx) in material.simple_rules" :key="idx" class="rule-item">
                        {{ rule }}
                      </li>
                    </ul>
                  </div>

                  <button class="btn-copy" @click.stop="copyToClipboard(material)">
                    📋 复制规则
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 版本信息 -->
        <section class="section">
          <h4>📜 版本信息</h4>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">当前版本:</span>
              <span class="value">v{{ policy.current_version_id }}</span>
            </div>
            <div class="info-item">
              <span class="label">创建时间:</span>
              <span class="value">{{ formatDate(policy.created_at) }}</span>
            </div>
            <div class="info-item">
              <span class="label">最后更新:</span>
              <span class="value">{{ formatDate(policy.updated_at) }}</span>
            </div>
          </div>
        </section>
      </div>

      <!-- 底部操作 -->
      <div class="modal-footer">
        <button class="btn-primary" @click="handleExport">📥 导出为JSON</button>
        <button class="btn-secondary" @click="handleVersionHistory">📜 版本历史</button>
        <button class="btn-close-modal" @click="$emit('close')">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  policy: {
    type: Object,
    required: true,
  },
})

defineEmits(['close'])

const showRaw = ref(false)
const expandedMaterial = ref(null)

const toggleMaterialDetail = (materialId) => {
  expandedMaterial.value = expandedMaterial.value === materialId ? null : materialId
}

const getMaterialLabel = (type) => {
  const labels = {
    ticketing_document: '📄 证件要求',
    medical_certificate: '🏥 诊断证明',
    hospital_records: '🏨 住院证明',
    inspection_report: '🔬 检查报告',
    medical_invoice: '💰 医疗发票',
    companion_proof: '👥 陪同人证明',
  }
  return labels[type] || type
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}

const copyToClipboard = (material) => {
  const text = `${getMaterialLabel(material.material_type)}\n\n定义:\n${material.definition}\n\n规则:\n${material.simple_rules.map(r => `• ${r}`).join('\n')}`
  navigator.clipboard.writeText(text)
  alert('✓ 已复制到剪贴板')
}

const handleExport = () => {
  const dataStr = JSON.stringify(props.policy, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${props.policy.airline_code}-policy.json`
  link.click()
  URL.revokeObjectURL(url)
}

const handleVersionHistory = () => {
  alert('🔄 版本历史功能 - 将在版本管理页面中详细展示')
}
</script>

<style scoped>
.detail-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.detail-modal {
  background: white;
  border-radius: 12px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.header-info h2 {
  margin: 0;
  font-size: 20px;
  color: #333;
  margin-bottom: 8px;
}

.badge {
  display: inline-block;
  background: #667eea;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
  transition: color 0.3s ease;
}

.btn-close:hover {
  color: #333;
}

.modal-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.section {
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.section-header:hover {
  background: #f0f0f0;
}

.section-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.toggle-icon {
  color: #667eea;
  font-size: 12px;
  transition: transform 0.3s ease;
}

.raw-policy {
  background: #f9f9f9;
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 16px;
  margin-top: 12px;
  max-height: 200px;
  overflow-y: auto;
  white-space: pre-wrap;
  font-size: 13px;
  color: #666;
  line-height: 1.6;
}

.subsection {
  margin: 16px 0;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 6px;
}

.subsection h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #333;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 8px;
  background: white;
  border-radius: 4px;
}

.label {
  font-weight: 600;
  color: #666;
}

.value {
  color: #333;
  font-weight: 500;
}

.materials-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.material-item {
  border: 1px solid #eee;
  border-radius: 6px;
  overflow: hidden;
  background: #f9f9f9;
}

.material-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.material-header:hover {
  background: #f0f0f0;
}

.material-type {
  font-weight: 600;
  color: #333;
}

.material-detail {
  padding: 16px;
  border-top: 1px solid #eee;
  background: white;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.definition,
.rules {
  margin-bottom: 12px;
}

.label-text {
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
  font-size: 13px;
}

.content-text {
  margin: 0;
  color: #666;
  font-size: 13px;
  line-height: 1.6;
}

.rules ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.rule-item {
  padding: 6px 0;
  color: #666;
  font-size: 13px;
  line-height: 1.5;
}

.rule-item:before {
  content: '• ';
  color: #667eea;
  font-weight: bold;
  margin-right: 8px;
}

.btn-copy {
  margin-top: 12px;
  padding: 8px 16px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s ease;
}

.btn-copy:hover {
  background: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #f0f0f0;
  background: #f9f9f9;
}

.btn-primary,
.btn-secondary,
.btn-close-modal {
  flex: 1;
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5568d3;
  transform: translateY(-2px);
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
  border: 1px solid #ddd;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.btn-close-modal {
  background: #f0f0f0;
  color: #333;
  border: 1px solid #ddd;
}

.btn-close-modal:hover {
  background: #e0e0e0;
}

@media (max-width: 768px) {
  .detail-modal {
    max-height: none;
    border-radius: 12px 12px 0 0;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .modal-footer {
    flex-wrap: wrap;
  }

  .btn-primary,
  .btn-secondary,
  .btn-close-modal {
    min-width: 100%;
  }
}
</style>
