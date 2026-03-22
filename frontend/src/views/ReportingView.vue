<template>
  <section class="reporting-view">
    <div v-if="loading" class="state-shell">
      <div class="state-card loading">
        <div class="shimmer-icon"></div>
        <div class="loading-content">
          <span class="state-label">Reporting</span>
          <h1>Preparing Dashboard</h1>
          <p>Analyzing ECO pipeline and engineering metrics...</p>
        </div>
      </div>
    </div>

    <div v-else-if="error" class="state-shell">
      <div class="state-card error">
        <AlertCircle class="error-icon" />
        <div class="error-content">
          <span class="state-label">Critical Error</span>
          <h1>Data Stream Interrupted</h1>
          <p>{{ error }}</p>
          <button @click="loadReporting" class="retry-btn">Try Reconnecting</button>
        </div>
      </div>
    </div>

    <template v-else>
      <header class="dashboard-header">
        <div class="header-main">
          <div class="badge-row">
            <span class="status-pill blue">
              <Activity :size="14" />
              Live System
            </span>
            <span class="timestamp">
              <Clock :size="14" />
              Updated recently
            </span>
          </div>
          <h1>{{ report.headline.title }}</h1>
          <p class="subtitle">{{ report.headline.subtitle }}</p>
        </div>
        
        <div class="header-stats">
          <div class="mini-kpi">
            <span class="label">Total ECOs</span>
            <strong class="value">{{ report.headline.total_ecos }}</strong>
          </div>
          <div class="mini-kpi primary">
            <span class="label">Completion</span>
            <strong class="value">{{ report.headline.completion_rate }}%</strong>
          </div>
        </div>
      </header>

      <section class="kpi-grid">
        <article
          v-for="item in report.status_mix"
          :key="item.label"
          class="kpi-card"
          :class="[`tone-${item.tone}`, { 'has-value': item.count > 0 }]"
        >
          <div class="kpi-icon-wrap">
            <component :is="statusIcon(item.label)" :size="20" />
          </div>
          <div class="kpi-content">
            <span class="kpi-label">{{ item.label }}</span>
            <strong class="kpi-value">{{ item.count }}</strong>
          </div>
          <div class="kpi-decoration" />
        </article>
      </section>

      <div class="dashboard-layout">
        <main class="primary-stack">
          <!-- Pipeline Section -->
          <section class="glass-panel pipeline-panel">
            <header class="panel-header">
              <div class="title-group">
                <BarChart3 :size="18" class="header-icon" />
                <h2>Stage Distribution</h2>
              </div>
              <p>Engineering Change Order progression through defined workflows.</p>
            </header>

            <div v-if="report.stage_breakdown.length" class="stage-container">
              <div v-for="stage in report.stage_breakdown" :key="stage.stage" class="stage-item">
                <div class="stage-info">
                  <div class="stage-name-wrap">
                    <span class="stage-name">{{ stage.stage }}</span>
                    <span class="stage-tag" :class="badgeTone(stage)">
                      {{ stage.count }}
                    </span>
                  </div>
                  <span class="stage-percent">{{ stage.percentage }}%</span>
                </div>
                <div class="progress-track">
                  <div 
                    class="progress-fill" 
                    :class="badgeTone(stage)" 
                    :style="{ width: `${stage.percentage}%` }"
                  >
                    <div class="fill-glow" />
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <p>No active pipeline data available.</p>
            </div>
          </section>

          <!-- Recent Activity -->
          <section class="glass-panel recent-panel">
            <header class="panel-header">
              <div class="title-group">
                <Activity :size="18" class="header-icon" />
                <h2>Recent Activity</h2>
              </div>
              <p>Handled engineering changes and system updates.</p>
            </header>

            <div v-if="report.recent_ecos.length" class="activity-feed dark-scrollbar">
              <button
                v-for="eco in report.recent_ecos"
                :key="eco.id"
                class="feed-item"
                @click="goToEco(eco.path)"
              >
                <div class="item-icon" :class="eco.type.toLowerCase()">
                  <component :is="eco.type.toLowerCase() === 'bom' ? Settings2 : Package" :size="16" />
                </div>
                <div class="item-body">
                  <div class="item-top">
                    <span class="item-name">{{ eco.name }}</span>
                    <span class="item-date">{{ formatDate(eco.created_at) }}</span>
                  </div>
                  <div class="item-meta">
                    <span class="item-stage">{{ eco.stage || 'Draft' }}</span>
                    <span class="dot" />
                    <span class="item-user">{{ eco.initiator }}</span>
                  </div>
                </div>
              </button>
            </div>
            <div v-else class="empty-mini">No recent ECO activity.</div>
          </section>

          <!-- ECO Type Composition (Moved inside stack) -->
          <section class="glass-panel mix-section">
            <header class="panel-header">
              <div class="title-group">
                <BarChart3 :size="18" class="header-icon" />
                <h2>ECO Type Composition</h2>
              </div>
              <p>Distribution across different engineering change categories.</p>
            </header>

            <div class="composition-grid">
              <div v-for="item in report.type_breakdown" :key="item.type" class="composition-card">
                <div class="comp-head">
                  <div class="comp-icon" :class="item.type.toLowerCase().includes('bom') ? 'bom' : 'product'">
                    <component :is="item.type.toLowerCase().includes('bom') ? Settings2 : Package" :size="14" />
                  </div>
                  <span class="comp-label">{{ item.type }}</span>
                  <strong class="comp-count">{{ item.count }}</strong>
                </div>
                <div class="comp-track">
                  <div class="comp-fill" :class="item.type.toLowerCase().includes('bom') ? 'bom' : 'product'" :style="{ width: `${item.percentage}%` }" />
                </div>
                <span class="comp-footer">{{ item.percentage }}% of total volume</span>
              </div>
            </div>
          </section>
        </main>

        <aside class="side-stack">
          <!-- Insights Card -->
          <article class="glass-panel highlight-panel">
            <header class="panel-header compact">
              <div class="title-group">
                <TrendingUp :size="18" class="header-icon" />
                <h2>Strategic Insights</h2>
              </div>
            </header>
            
            <div class="insight-grid">
              <div v-for="insight in report.insights" :key="insight.label" class="insight-card" :class="`tone-${insight.tone}`">
                <span class="insight-title">{{ insight.label }}</span>
                <strong class="insight-data">{{ insight.value }}</strong>
              </div>
            </div>
          </article>

          <!-- Output Metrics -->
          <article class="glass-panel output-panel">
            <header class="panel-header compact">
              <div class="title-group">
                <ClipboardList :size="18" class="header-icon" />
                <h2>Revision Output</h2>
              </div>
            </header>
            
            <div class="impact-metrics">
              <div class="impact-box">
                <div class="impact-head">
                  <Package :size="16" />
                  <span>Product Versions</span>
                </div>
                <strong class="impact-val">{{ report.impact.eco_product_versions }}</strong>
                <div class="impact-share">
                  <div class="share-bar"><div class="share-fill" :style="{ width: `${report.impact.product_share}%` }" /></div>
                  <span>{{ report.impact.product_share }}%</span>
                </div>
              </div>
              <div class="impact-box">
                <div class="impact-head">
                  <Settings2 :size="16" />
                  <span>Bill of Materials</span>
                </div>
                <strong class="impact-val">{{ report.impact.eco_boms }}</strong>
                <div class="impact-share">
                  <div class="share-bar"><div class="share-fill" :style="{ width: `${report.impact.bom_share}%` }" /></div>
                  <span>{{ report.impact.bom_share }}%</span>
                </div>
              </div>
            </div>
          </article>
          <!-- Workload Section -->
          <article class="glass-panel load-panel">
            <header class="panel-header compact">
              <div class="title-group">
                <Users :size="18" class="header-icon" />
                <h2>Approval Load</h2>
              </div>
            </header>
            
            <div v-if="report.approval_workload.length" class="load-list">
              <div v-for="row in report.approval_workload" :key="row.user_id" class="load-row">
                <div class="load-user">
                  <div class="user-avatar">{{ row.user_name.charAt(0) }}</div>
                  <span class="user-name">{{ row.user_name }}</span>
                </div>
                <span class="load-count" :class="{ warning: row.pending_count > 5 }">{{ row.pending_count }}</span>
              </div>
            </div>
            <p v-else class="empty-mini">Zero pending assignments.</p>
          </article>
        </aside>
      <!-- Grid Ends -->
      </div>
    </template>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/core/api';
import { useBreadcrumbs } from '@/composables/useBreadcrumbs';
import { 
  ClipboardList, 
  Activity, 
  CheckCircle2, 
  AlertCircle, 
  Clock, 
  Users, 
  Package, 
  Settings2, 
  TrendingUp, 
  BarChart3,
  FileText
} from 'lucide-vue-next';

interface ReportingOverview {
  headline: {
    title: string;
    subtitle: string;
    total_ecos: number;
    completion_rate: number;
    pending_approvals: number;
    created_last_7_days: number;
    dominant_stage: string;
  };
  kpis: any;
  stage_breakdown: any[];
  type_breakdown: any[];
  impact: any;
  insights: any[];
  status_mix: any[];
  recent_ecos: any[];
  approval_workload: any[];
}

const router = useRouter();
const { push: pushBc } = useBreadcrumbs();

const report = ref<ReportingOverview>({
  headline: {
    title: '',
    subtitle: '',
    total_ecos: 0,
    completion_rate: 0,
    pending_approvals: 0,
    created_last_7_days: 0,
    dominant_stage: '',
  },
  kpis: {},
  stage_breakdown: [],
  type_breakdown: [],
  impact: {
    eco_product_versions: 0,
    eco_boms: 0,
    product_share: 0,
    bom_share: 0,
  },
  insights: [],
  status_mix: [],
  recent_ecos: [],
  approval_workload: [],
});

const loading = ref(true);
const error = ref('');

const statusIcon = (label: string) => {
  const l = label.toLowerCase();
  if (l.includes('draft')) return FileText;
  if (l.includes('progress')) return Clock;
  if (l.includes('done')) return CheckCircle2;
  if (l.includes('refused')) return AlertCircle;
  return Activity;
};

const badgeTone = (stage: any) => {
  if (stage.is_refused) return 'danger';
  if (stage.is_last) return 'success';
  if (report.value.stage_breakdown.length > 0 && stage.sequence === Math.min(...report.value.stage_breakdown.map((item: any) => item.sequence))) return 'info';
  return 'primary';
};

const formatDate = (value: string | null) => {
  if (!value) return '-';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '-';

  return new Intl.DateTimeFormat(undefined, {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  }).format(date);
};

const goToEco = (path: string) => {
  if (!path) return;
  pushBc({ label: 'Reporting', path: '/reporting' });
  router.push(path);
};

const loadReporting = async () => {
  loading.value = true;
  error.value = '';

  try {
    const response = await api.get('/models/reporting/overview');
    report.value = response.data;
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to connect to reporting services.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadReporting();
});
</script>

<style lang="scss" scoped>
@use "../styles/variables" as v;

.reporting-view {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  height: 100%;
  min-height: 0;
  overflow-y: auto;
  padding: 1.5rem 2rem 3rem;
  background: var(--bg-main);
  color: var(--text-primary);
  scrollbar-gutter: stable;
}

// State Shells
.state-shell {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.state-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  padding: 3rem;
  border-radius: 2rem;
  display: flex;
  align-items: center;
  gap: 2rem;
  box-shadow: var(--shadow-lg);
  max-width: 600px;
  width: 100%;

  &.loading {
    .shimmer-icon {
      width: 64px;
      height: 64px;
      border-radius: 1.5rem;
      background: linear-gradient(90deg, var(--bg-tertiary) 25%, var(--border-light) 50%, var(--bg-tertiary) 75%);
      background-size: 200% 100%;
      animation: shimmer 1.5s infinite;
    }
  }

  &.error {
    border-color: rgba(220, 38, 38, 0.3);
    .error-icon {
      width: 64px;
      height: 64px;
      color: var(--danger-color);
    }
  }

  .state-label {
    text-transform: uppercase;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    color: var(--text-tertiary);
    margin-bottom: 0.5rem;
    display: block;
  }

  h1 {
    font-size: 1.75rem;
    margin-bottom: 0.75rem;
    font-weight: 700;
  }

  p {
    color: var(--text-secondary);
    line-height: 1.6;
  }
}

// Header
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 2rem;
  padding-bottom: 0.5rem;

  .header-main {
    h1 {
      font-size: 2.5rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin: 0.5rem 0;
      background: linear-gradient(135deg, var(--text-primary) 0%, var(--text-secondary) 100%);
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .subtitle {
      font-size: 1.1rem;
      color: var(--text-secondary);
      max-width: 600px;
    }
  }

  .badge-row {
    display: flex;
    gap: 1rem;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .header-stats {
    display: flex;
    gap: 1.5rem;
  }
}

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.75rem;
  border-radius: 2rem;
  font-size: 0.75rem;
  font-weight: 600;
  
  &.blue {
    background: rgba(37, 99, 235, 0.1);
    color: #3b82f6;
  }
}

.timestamp {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.75rem;
  color: var(--text-tertiary);
}

.mini-kpi {
  text-align: right;
  .label {
    display: block;
    font-size: 0.7rem;
    text-transform: uppercase;
    font-weight: 700;
    color: var(--text-tertiary);
    margin-bottom: 0.2rem;
  }
  .value {
    font-size: 1.5rem;
    font-weight: 800;
  }
  &.primary .value {
    color: var(--primary-color);
  }
}

// KPI Grid
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
}

.kpi-card {
  position: relative;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  padding: 1.5rem;
  border-radius: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;

  &:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
    border-color: var(--primary-color);
  }

  .kpi-icon-wrap {
    width: 48px;
    height: 48px;
    border-radius: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg-tertiary);
    color: var(--text-secondary);
    transition: all 0.3s;
  }

  .kpi-label {
    display: block;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-secondary);
  }

  .kpi-value {
    font-size: 1.75rem;
    font-weight: 800;
    line-height: 1;
  }

  .kpi-decoration {
    position: absolute;
    bottom: -10px;
    right: -10px;
    width: 60px;
    height: 60px;
    background: currentColor;
    opacity: 0.03;
    border-radius: 50%;
  }

  &.tone-info { .kpi-icon-wrap { color: #0ea5e9; background: rgba(14, 165, 233, 0.08); } }
  &.tone-primary { .kpi-icon-wrap { color: #3b82f6; background: rgba(59, 130, 246, 0.08); } }
  &.tone-success { .kpi-icon-wrap { color: #10b981; background: rgba(16, 185, 129, 0.08); } }
  &.tone-warning { .kpi-icon-wrap { color: #f59e0b; background: rgba(245, 158, 11, 0.08); } }
  &.tone-danger { .kpi-icon-wrap { color: #ef4444; background: rgba(239, 68, 68, 0.08); } }

  &.has-value:hover {
    &.tone-success { border-color: #10b981; }
    &.tone-info { border-color: #0ea5e9; }
    &.tone-danger { border-color: #ef4444; }
  }
}

// Layout
.dashboard-layout {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 2rem;

  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
  }
}

.primary-stack, .side-stack {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  height: 100%;
}

// Global Panel Styles
.glass-panel {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 1.5rem;
  padding: 1.75rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);

  [data-theme="dark"] & {
    background: rgba(30, 41, 59, 0.4);
    backdrop-filter: blur(12px);
    border-color: rgba(255, 255, 255, 0.05);
  }
}

.panel-header {
  margin-bottom: 2rem;
  
  .title-group {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.35rem;

    .header-icon {
      color: var(--primary-color);
    }

    h2 {
      font-size: 1.25rem;
      font-weight: 700;
      margin: 0;
    }
  }

  p {
    font-size: 0.9rem;
    color: var(--text-tertiary);
    margin: 0;
  }

  &.compact {
    margin-bottom: 1.5rem;
  }
}

// Pipeline
.stage-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.stage-item {
  .stage-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.65rem;
  }
  
  .stage-name-wrap {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .stage-name {
    font-weight: 600;
    font-size: 0.95rem;
  }

  .stage-tag {
    font-size: 0.7rem;
    font-weight: 800;
    padding: 0.2rem 0.5rem;
    border-radius: 0.5rem;
    background: var(--bg-tertiary);
    color: var(--text-secondary);

    &.primary { background: rgba(59, 130, 246, 0.1); color: #3b82f6; }
    &.success { background: rgba(16, 185, 129, 0.1); color: #10b981; }
    &.info { background: rgba(14, 165, 233, 0.1); color: #0ea5e9; }
    &.danger { background: rgba(239, 68, 68, 0.1); color: #ef4444; }
  }

  .stage-percent {
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--text-tertiary);
  }
}

.progress-track {
  height: 8px;
  background: var(--bg-tertiary);
  border-radius: 1rem;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 1rem;
  position: relative;
  transition: width 1s ease-out;

  &.primary { background: linear-gradient(90deg, #60a5fa, #3b82f6); }
  &.success { background: linear-gradient(90deg, #34d399, #10b981); }
  &.info { background: linear-gradient(90deg, #38bdf8, #0ea5e9); }
  &.danger { background: linear-gradient(90deg, #f87171, #ef4444); }

  .fill-glow {
    position: absolute;
    top: 0; right: 0; bottom: 0; left: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    animation: flow 2s infinite linear;
  }
}

.load-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.output-panel {
  // Let it be natural
}

.recent-panel {
  // Let it be natural
}

.mix-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.activity-feed {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  overflow-y: auto;
  padding-right: 0.5rem;
  max-height: 600px;
}

.feed-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-tertiary);
  border: 1px solid transparent;
  border-radius: 1rem;
  text-align: left;
  transition: all 0.2s;

  &:hover {
    background: var(--bg-secondary);
    border-color: var(--border-color);
    transform: translateX(4px);
    box-shadow: var(--shadow-sm);
  }

  .item-icon {
    width: 36px;
    height: 36px;
    border-radius: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    
    &.PRODUCT { background: rgba(var(--primary-color-rgb, 37, 99, 235), 0.1); color: var(--primary-color); }
    &.BOM { background: rgba(139, 92, 246, 0.1); color: #8b5cf6; }
  }

  .item-body {
    flex-grow: 1;
    min-width: 0;
  }

  .item-top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.25rem;
  }

  .item-name {
    font-weight: 700;
    font-size: 0.95rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .item-date {
    font-size: 0.75rem;
    color: var(--text-tertiary);
    font-weight: 500;
  }

  .item-meta {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8rem;
    color: var(--text-secondary);

    .dot {
      width: 3px;
      height: 3px;
      background: var(--text-tertiary);
      border-radius: 50%;
    }
  }
}

// Insights
.insight-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.insight-card {
  padding: 1.25rem;
  background: var(--bg-tertiary);
  border-left: 4px solid var(--border-color);
  border-radius: 0.75rem;

  .insight-title {
    display: block;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--text-tertiary);
    margin-bottom: 0.5rem;
  }

  .insight-data {
    font-size: 1.15rem;
    font-weight: 800;
    line-height: 1.2;
  }

  &.tone-primary { border-left-color: #3b82f6; }
  &.tone-success { border-left-color: #10b981; }
  &.tone-warning { border-left-color: #f59e0b; }
}

// Impact Metrics
.impact-metrics {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
}

.impact-box {
  padding: 1.25rem;
  background: var(--bg-tertiary);
  border-radius: 1rem;

  .impact-head {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
  }

  .impact-val {
    font-size: 2rem;
    font-weight: 800;
    display: block;
    margin-bottom: 1rem;
  }
}

.impact-share {
  display: flex;
  align-items: center;
  gap: 1rem;

  .share-bar {
    flex-grow: 1;
    height: 4px;
    background: var(--border-color);
    border-radius: 2px;
    overflow: hidden;
  }

  .share-fill {
    height: 100%;
    background: var(--primary-color);
  }

  span {
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--text-secondary);
  }
}

// Workload
.load-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.load-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: var(--bg-tertiary);
  border-radius: 0.75rem;

  .load-user {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .user-avatar {
    width: 28px;
    height: 28px;
    background: var(--primary-color);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
  }

  .user-name {
    font-size: 0.9rem;
    font-weight: 600;
  }

  .load-count {
    font-size: 0.85rem;
    font-weight: 800;
    color: var(--text-primary);
    background: var(--bg-secondary);
    padding: 0.2rem 0.6rem;
    border-radius: 0.5rem;

    &.warning {
      background: rgba(239, 68, 68, 0.1);
      color: #ef4444;
    }
  }
}

// Composition
.mix-section {
  margin-top: 1rem;
}

.composition-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.composition-card {
  padding: 1.5rem;
  background: var(--bg-tertiary);
  border-radius: 1.25rem;

  .comp-head {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
  }

  .comp-icon {
    width: 32px;
    height: 32px;
    border-radius: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    &.product { background: rgba(var(--primary-color-rgb, 37, 99, 235), 0.1); color: var(--primary-color); }
    &.bom { background: rgba(139, 92, 246, 0.1); color: #8b5cf6; }
  }

  .comp-label {
    flex-grow: 1;
    font-weight: 600;
    font-size: 0.9rem;
  }

  .comp-count {
    font-size: 1.25rem;
    font-weight: 800;
  }

  .comp-track {
    height: 6px;
    background: var(--border-color);
    border-radius: 3px;
    margin-bottom: 0.5rem;
    overflow: hidden;
  }

  .comp-fill {
    height: 100%;
    &.product { background: var(--primary-color); }
    &.bom { background: #8b5cf6; }
  }

  .comp-footer {
    font-size: 0.75rem;
    color: var(--text-tertiary);
    font-weight: 500;
  }
}

// Utilities
.empty-state, .empty-mini {
  padding: 3rem;
  text-align: center;
  color: var(--text-tertiary);
  background: var(--bg-tertiary);
  border-radius: 1rem;
  border: 1px dashed var(--border-color);
}

.empty-mini {
  padding: 1.5rem;
  font-size: 0.85rem;
}

.retry-btn {
  margin-top: 1.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
  &:hover { opacity: 0.9; }
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@keyframes flow {
  from { transform: translateX(-100%); }
  to { transform: translateX(100%); }
}
</style>
