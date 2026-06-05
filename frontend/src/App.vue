<template>
  <div class="app-container">
    <!-- 装饰背景 -->
    <div class="bg-blur bg-blur-1"></div>
    <div class="bg-blur bg-blur-2"></div>
    <div class="bg-blur bg-blur-3"></div>

    <header class="app-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="app-title">病退政策</h1>
          <p class="app-subtitle">管理系统</p>
        </div>
        <nav class="app-nav">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            :class="['nav-btn', { active: activeTab === tab.id }]"
            @click="activeTab = tab.id"
          >
            {{ tab.label }}
          </button>
        </nav>
      </div>
    </header>

    <main class="app-main">
      <!-- 政策检索页面 -->
      <section v-show="activeTab === 'search'" class="page">
        <PolicySearch />
      </section>

      <!-- 版本管理页面 -->
      <section v-show="activeTab === 'versions'" class="page">
        <VersionManage />
      </section>

      <!-- 统计页面 -->
      <section v-show="activeTab === 'stats'" class="page">
        <StatsView />
      </section>
    </main>

    <footer class="app-footer">
      <p>病退政策管理系统 v1.0.0</p>
      <p class="footer-meta">实时更新 • 版本管理 • 多AI接入</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { usePolicyStore } from './stores/policyStore'
import PolicySearch from './components/PolicySearch.vue'
import VersionManage from './components/VersionManage.vue'
import StatsView from './components/StatsView.vue'

const activeTab = ref('search')
const policyStore = usePolicyStore()

const tabs = [
  { id: 'search', label: '📋 政策检索' },
  { id: 'versions', label: '📜 版本管理' },
  { id: 'stats', label: '📊 统计信息' },
]

onMounted(async () => {
  await policyStore.fetchPolicies()
  await policyStore.fetchStats()
})
</script>

<style>
:root {
  /* Morandi Color Palette */
  --color-primary: #5b7a6b;      /* 墨绿 - Primary */
  --color-primary-light: #7a9684; /* 浅墨绿 */
  --color-secondary: #c4a5a0;    /* 樱花粉 - Secondary */
  --color-accent: #8b7d7a;       /* 雾灰 - Accent */
  --color-dark: #3d3d3d;         /* 深灰 */
  --color-light: #f5f3f0;        /* 米色背景 */
  --color-card: #fefdfb;         /* 奶油白 */

  /* Glass effect */
  --glass-bg: rgba(254, 253, 251, 0.7);
  --glass-border: rgba(255, 255, 255, 0.3);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style>

<style scoped>
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f3f0 0%, #ede8e3 100%);
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

/* 水彩背景装饰 */
.bg-blur {
  position: fixed;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
  z-index: 0;
}

.bg-blur-1 {
  width: 600px;
  height: 600px;
  background: var(--color-primary);
  top: -200px;
  left: -200px;
}

.bg-blur-2 {
  width: 500px;
  height: 500px;
  background: var(--color-secondary);
  bottom: -150px;
  right: -150px;
}

.bg-blur-3 {
  width: 400px;
  height: 400px;
  background: var(--color-accent);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.app-header {
  position: relative;
  z-index: 10;
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--glass-border);
  padding: 32px 0;
  box-shadow: 0 8px 32px rgba(91, 122, 107, 0.08);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
}

.title-section {
  flex: 1;
}

.app-title {
  color: var(--color-primary);
  font-size: 32px;
  margin: 0 0 4px 0;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.app-subtitle {
  color: var(--color-accent);
  font-size: 14px;
  margin: 0;
  font-weight: 400;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.app-nav {
  display: flex;
  gap: 12px;
}

.nav-btn {
  padding: 12px 24px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  color: var(--color-dark);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  font-size: 14px;
  font-weight: 600;
  position: relative;
  overflow: hidden;
}

.nav-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: rgba(91, 122, 107, 0.1);
  transition: left 0.4s ease;
  z-index: -1;
}

.nav-btn:hover {
  border-color: var(--color-primary);
  transform: translateY(-4px);
}

.nav-btn:hover::before {
  left: 0;
}

.nav-btn.active {
  background: var(--color-primary);
  color: var(--color-card);
  border-color: var(--color-primary);
  box-shadow: 0 12px 28px rgba(91, 122, 107, 0.25);
}

.app-main {
  flex: 1;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 48px 40px;
  position: relative;
  z-index: 5;
  animation: fadeIn 0.6s ease-out;
}

.page {
  animation: slideUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.app-footer {
  position: relative;
  z-index: 10;
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  color: var(--color-accent);
  text-align: center;
  padding: 32px 20px;
  border-top: 1px solid var(--glass-border);
  font-size: 12px;
}

.app-footer p {
  margin: 0;
}

.app-footer .footer-meta {
  margin-top: 8px;
  letter-spacing: 1px;
  font-size: 11px;
  color: var(--color-accent);
  opacity: 0.7;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 20px;
    padding: 0 20px;
  }

  .app-title {
    font-size: 24px;
  }

  .app-nav {
    flex-wrap: wrap;
    width: 100%;
  }

  .nav-btn {
    flex: 1;
    min-width: 120px;
  }

  .app-main {
    padding: 24px 20px;
  }
}
</style>
