<template>
  <div class="stats-view">
    <div class="stats-grid">
      <!-- 总政策数 -->
      <div class="stat-card">
        <div class="stat-icon">📋</div>
        <div class="stat-content">
          <h3>总政策数</h3>
          <p class="stat-value">{{ policyStore.stats?.total_policies || 0 }}</p>
          <p class="stat-label">个航司政策</p>
        </div>
      </div>

      <!-- 总版本数 -->
      <div class="stat-card">
        <div class="stat-icon">📜</div>
        <div class="stat-content">
          <h3>总版本数</h3>
          <p class="stat-value">{{ policyStore.stats?.total_versions || 0 }}</p>
          <p class="stat-label">个历史版本</p>
        </div>
      </div>

      <!-- 航司数 -->
      <div class="stat-card">
        <div class="stat-icon">✈️</div>
        <div class="stat-content">
          <h3>覆盖航司</h3>
          <p class="stat-value">{{ policyStore.stats?.total_airlines || 0 }}</p>
          <p class="stat-label">家航空公司</p>
        </div>
      </div>

      <!-- 平均版本 -->
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <h3>平均版本数</h3>
          <p class="stat-value">
            {{
              policyStore.stats
                ? (policyStore.stats.total_versions / policyStore.stats.total_policies).toFixed(1)
                : 0
            }}
          </p>
          <p class="stat-label">版本/政策</p>
        </div>
      </div>
    </div>

    <!-- 详细信息 -->
    <div class="detail-section">
      <h2>📈 系统概览</h2>

      <div class="info-box">
        <h4>✓ 功能特性</h4>
        <ul class="feature-list">
          <li>✓ 实时政策更新</li>
          <li>✓ 完整版本历史</li>
          <li>✓ 一键回滚机制</li>
          <li>✓ 操作审计日志</li>
          <li>✓ 多AI接入支持</li>
          <li>✓ 导入/导出功能</li>
        </ul>
      </div>

      <div class="info-box">
        <h4>📌 快速链接</h4>
        <div class="links">
          <a href="http://localhost:8000/docs" target="_blank" class="link">🔗 API 文档 (Swagger)</a>
          <a href="http://localhost:8000/redoc" target="_blank" class="link">🔗 ReDoc 文档</a>
          <a href="" class="link">📞 联系支持</a>
        </div>
      </div>

      <div class="info-box">
        <h4>🚀 下一步计划</h4>
        <ul class="plan-list">
          <li>🔄 WebSocket 实时同步</li>
          <li>🤖 Webhook 多AI接入</li>
          <li>🌍 国际化支持</li>
          <li>📱 移动端适配</li>
          <li>🔔 实时通知系统</li>
        </ul>
      </div>
    </div>

    <!-- 刷新按钮 -->
    <div class="action-bar">
      <button class="btn-refresh" @click="handleRefresh">
        🔄 刷新统计信息
      </button>
    </div>
  </div>
</template>

<script setup>
import { usePolicyStore } from '../stores/policyStore'

const policyStore = usePolicyStore()

const handleRefresh = async () => {
  await policyStore.fetchStats()
  alert('✓ 统计信息已刷新')
}
</script>

<style scoped>
.stats-view {
  animation: fadeIn 0.6s ease-out;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.stat-card {
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: 28px;
  display: flex;
  gap: 16px;
  box-shadow: 0 8px 32px rgba(91, 122, 107, 0.08);
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  animation: cardSlideIn 0.6s ease-out backwards;
}

.stat-card:nth-child(1) {
  animation-delay: 0.05s;
}

.stat-card:nth-child(2) {
  animation-delay: 0.1s;
}

.stat-card:nth-child(3) {
  animation-delay: 0.15s;
}

.stat-card:nth-child(4) {
  animation-delay: 0.2s;
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

.stat-card:hover {
  transform: translateY(-8px);
  border-color: var(--color-primary);
  box-shadow: 0 16px 48px rgba(91, 122, 107, 0.16);
}

.stat-icon {
  font-size: 36px;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-content h3 {
  margin: 0 0 8px 0;
  font-size: 13px;
  color: var(--color-accent);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  margin: 10px 0;
  font-size: 32px;
  font-weight: 700;
  color: var(--color-primary);
  line-height: 1;
}

.stat-label {
  margin: 6px 0 0 0;
  font-size: 12px;
  color: var(--color-accent);
}

.detail-section {
  margin-top: 50px;
}

.detail-section h2 {
  color: var(--color-primary);
  margin: 0 0 28px 0;
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.3px;
}

.info-box {
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: 28px;
  margin-bottom: 24px;
  box-shadow: 0 8px 32px rgba(91, 122, 107, 0.08);
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.info-box h4 {
  margin: 0 0 18px 0;
  font-size: 15px;
  color: var(--color-primary);
  font-weight: 700;
  letter-spacing: 0.3px;
}

.feature-list,
.plan-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.feature-list li,
.plan-list li {
  padding: 10px 0;
  color: var(--color-accent);
  font-size: 14px;
  line-height: 1.6;
}

.links {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.link {
  display: inline-block;
  padding: 11px 16px;
  background: rgba(91, 122, 107, 0.05);
  border: 1px solid rgba(91, 122, 107, 0.15);
  border-radius: 10px;
  color: var(--color-primary);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.link:hover {
  background: rgba(91, 122, 107, 0.1);
  border-color: var(--color-primary);
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(91, 122, 107, 0.12);
}

.action-bar {
  margin-top: 40px;
  display: flex;
  justify-content: center;
}

.btn-refresh {
  padding: 12px 32px;
  background: var(--color-secondary);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-refresh:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(196, 165, 160, 0.2);
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
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stat-card {
    flex-direction: column;
    text-align: center;
  }

  .stat-icon {
    font-size: 40px;
  }

  .detail-section h2 {
    font-size: 18px;
  }
}
</style>
