<template>
  <div class="confirm-overlay" @click.self="$emit('cancel')">
    <div class="confirm-dialog">
      <div class="confirm-header">
        <h3>确认回滚</h3>
      </div>

      <div class="confirm-content">
        <div class="warning-box">
          此操作将把政策回滚到以前的版本。当前版本的所有更改都会被还原。
        </div>

        <div class="version-compare">
          <div class="version-box current">
            <h4>当前版本</h4>
            <p class="version-tag">{{ currentVersion.version_tag }}</p>
            <p class="version-info">{{ currentVersion.changes_summary }}</p>
          </div>

          <div class="arrow">⟹</div>

          <div class="version-box target">
            <h4>目标版本</h4>
            <p class="version-tag">{{ targetVersion.version_tag }}</p>
            <p class="version-info">{{ targetVersion.changes_summary }}</p>
          </div>
        </div>

        <div class="operator-input">
          <label>操作者:</label>
          <input
            v-model="operator"
            type="text"
            placeholder="请输入您的名称或ID"
            class="input"
          />
        </div>
      </div>

      <div class="confirm-footer">
        <button class="btn-cancel" @click="$emit('cancel')">取消</button>
        <button class="btn-confirm" @click="handleConfirm" :disabled="!operator">
          确认回滚
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  currentVersion: {
    type: Object,
    required: true,
  },
  targetVersion: {
    type: Object,
    required: true,
  },
  policyId: {
    type: Number,
    required: true,
  },
})

const emit = defineEmits(['confirm', 'cancel'])
const operator = ref('')

const handleConfirm = () => {
  if (!operator.value.trim()) {
    alert('请输入操作者信息')
    return
  }
  emit('confirm', operator.value)
}
</script>

<style scoped>
.confirm-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(61, 61, 61, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
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

.confirm-dialog {
  background: var(--color-card);
  border-radius: 16px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(91, 122, 107, 0.2);
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

.confirm-header {
  padding: 24px 24px 16px;
  border-bottom: 1px solid rgba(91, 122, 107, 0.1);
}

.confirm-header h3 {
  margin: 0;
  font-size: 16px;
  color: var(--color-primary);
  font-weight: 700;
}

.confirm-content {
  padding: 24px;
}

.warning-box {
  background: rgba(196, 165, 160, 0.1);
  border: 1px solid rgba(196, 165, 160, 0.3);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 20px;
  font-size: 13px;
  color: var(--color-accent);
  line-height: 1.5;
}

.version-compare {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.version-box {
  flex: 1;
  border: 1px solid rgba(91, 122, 107, 0.2);
  border-radius: 8px;
  padding: 12px;
  background: rgba(91, 122, 107, 0.05);
}

.version-box h4 {
  margin: 0 0 8px 0;
  font-size: 12px;
  color: var(--color-accent);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.version-tag {
  margin: 0 0 6px 0;
  font-family: 'Courier New', monospace;
  font-weight: 700;
  color: var(--color-primary);
  font-size: 12px;
}

.version-info {
  margin: 0;
  font-size: 11px;
  color: var(--color-accent);
  line-height: 1.4;
}

.version-box.target {
  border-color: rgba(196, 165, 160, 0.3);
  background: rgba(196, 165, 160, 0.05);
}

.arrow {
  font-size: 18px;
  color: var(--color-secondary);
  flex-shrink: 0;
}

.operator-input {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.operator-input label {
  font-weight: 600;
  color: var(--color-primary);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.input {
  padding: 10px 12px;
  border: 1px solid rgba(91, 122, 107, 0.2);
  border-radius: 8px;
  font-size: 13px;
  background: rgba(245, 243, 240, 0.5);
  color: var(--color-dark);
  transition: all 0.3s ease;
  font-family: inherit;
}

.input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(91, 122, 107, 0.1);
  outline: none;
  background: white;
}

.confirm-footer {
  display: flex;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid rgba(91, 122, 107, 0.1);
  background: rgba(245, 243, 240, 0.3);
}

.btn-cancel,
.btn-confirm {
  flex: 1;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-cancel {
  background: rgba(91, 122, 107, 0.1);
  color: var(--color-primary);
  border: 1px solid rgba(91, 122, 107, 0.2);
}

.btn-cancel:hover {
  background: rgba(91, 122, 107, 0.15);
}

.btn-confirm {
  background: var(--color-secondary);
  color: white;
}

.btn-confirm:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(196, 165, 160, 0.3);
}

.btn-confirm:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
