<template>
  <div class="comparison-view">
    <div v-if="loading" class="comparison-state">
      <div class="loading-spinner"></div>
      <span>Loading comparison...</span>
    </div>
    <div v-else-if="error" class="comparison-state comparison-error">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="9" stroke="currentColor" stroke-width="1.5"/><path d="M10 6v5M10 13.5v.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
      <span>{{ error }}</span>
    </div>
    <div v-else-if="comparison" class="comparison-content">
      <!-- Hero Header -->
      <div class="comparison-header">
        <div class="header-left">
          <div class="header-text">
            <span class="header-eyebrow">Comparison View</span>
            <h1 class="header-title">{{ comparison.title }}</h1>
            <p class="header-subtitle" v-if="comparison.subtitle">{{ comparison.subtitle }}</p>
          </div>
        </div>
      </div>

      <!-- Main Sheet -->
      <div class="comparison-sheet">
        <!-- Summary Stats -->
        <div class="summary-row">
          <div class="stat-card" :class="{ active: comparison.summary?.changed_fields }">
            <div class="stat-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            </div>
            <div class="stat-content">
              <span class="stat-label">Field Changes</span>
              <span class="stat-value">{{ comparison.summary?.changed_fields || 0 }}</span>
            </div>
          </div>
          <div class="stat-card" :class="{ active: comparison.summary?.component_changes }">
            <div class="stat-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
            </div>
            <div class="stat-content">
              <span class="stat-label">Components</span>
              <span class="stat-value">{{ comparison.summary?.component_changes || 0 }}</span>
            </div>
          </div>
          <div class="stat-card" :class="{ active: comparison.summary?.workorder_changes }">
            <div class="stat-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/></svg>
            </div>
            <div class="stat-content">
              <span class="stat-label">Operations</span>
              <span class="stat-value">{{ comparison.summary?.workorder_changes || 0 }}</span>
            </div>
          </div>
          <div class="stat-card" :class="{ active: comparison.summary?.comparisons }">
            <div class="stat-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
            </div>
            <div class="stat-content">
              <span class="stat-label">History Points</span>
              <span class="stat-value">{{ comparison.summary?.comparisons || 0 }}</span>
            </div>
          </div>
        </div>

        <!-- Unified Comparison Table -->
        <div class="diff-master-container">
          <!-- Pair Mode -->
          <template v-if="comparison.mode === 'pair'">
            <div class="unified-diff-table">
              <!-- Version Row Header -->
              <div class="diff-table-header version-row">
                <div class="diff-col-field info-col">
                  <div class="info-label">VERSION INFO</div>
                </div>
                <div class="diff-col-old version-col">
                  <div class="version-hero v-old">
                    <span class="v-label">VERSION</span>
                    <span class="v-number">{{ comparison.old_record?.version || 'OLD' }}</span>
                    <div class="v-status" :class="comparison.old_record?.state">{{ comparison.old_record?.state }}</div>
                  </div>
                  <div class="v-details">{{ comparison.old_record?.name }}</div>
                </div>
                <div class="diff-col-new version-col">
                  <div class="version-hero v-new">
                    <span class="v-label">VERSION</span>
                    <span class="v-number">{{ comparison.new_record?.version || 'NEW' }}</span>
                    <div class="v-status" :class="comparison.new_record?.state">{{ comparison.new_record?.state }}</div>
                  </div>
                  <div class="v-details">{{ comparison.new_record?.name }}</div>
                </div>
              </div>

              <!-- Field Changes Group -->
              <template v-if="comparison.field_changes?.length">
                <div class="group-separator field-group">
                  <div class="separator-content">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                    Field Changes
                    <span class="pill">{{ comparison.field_changes.length }}</span>
                  </div>
                </div>
                <div v-for="item in comparison.field_changes" :key="item.field" class="diff-table-row">
                  <div class="diff-col-field">{{ item.label }}</div>
                  <div class="diff-col-old"><span class="val-cell old-cell">{{ item.old_value || '—' }}</span></div>
                  <div class="diff-col-new"><span class="val-cell new-cell">{{ item.new_value || '—' }}</span></div>
                </div>
              </template>

              <!-- Component Changes Group -->
              <template v-if="comparison.component_changes?.length">
                <div class="group-separator component-group">
                  <div class="separator-content">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
                    Component Changes
                    <span class="pill">{{ comparison.component_changes.length }}</span>
                  </div>
                </div>
                <div v-for="item in comparison.component_changes" :key="`comp-${item.label}`" class="diff-table-row" :class="item.change_type">
                  <div class="diff-col-field">
                    <span class="change-type-badge" :class="item.change_type" v-if="item.change_type">{{ item.change_type }}</span>
                    {{ item.label }}
                  </div>
                  <div class="diff-col-old"><span class="val-cell old-cell">{{ formatStructured(item.old_value) }}</span></div>
                  <div class="diff-col-new"><span class="val-cell new-cell">{{ formatStructured(item.new_value) }}</span></div>
                </div>
              </template>

              <!-- Work Order Changes Group -->
              <template v-if="comparison.workorder_changes?.length">
                <div class="group-separator operation-group">
                  <div class="separator-content">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/></svg>
                    Operation Changes
                    <span class="pill">{{ comparison.workorder_changes.length }}</span>
                  </div>
                </div>
                <div v-for="item in comparison.workorder_changes" :key="`wo-${item.label}`" class="diff-table-row" :class="item.change_type">
                  <div class="diff-col-field">
                    <span class="change-type-badge" :class="item.change_type" v-if="item.change_type">{{ item.change_type }}</span>
                    {{ item.label }}
                  </div>
                  <div class="diff-col-old"><span class="val-cell old-cell">{{ formatStructured(item.old_value) }}</span></div>
                  <div class="diff-col-new"><span class="val-cell new-cell">{{ formatStructured(item.new_value) }}</span></div>
                </div>
              </template>
            </div>
          </template>

          <!-- Version History Mode -->
          <template v-else-if="comparison.mode === 'version_history'">
            <div class="unified-diff-table history-mode">
              <template v-for="item in comparison.comparisons || []" :key="item.target.id">
                <div class="group-separator history-top">
                  <div class="separator-content">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                    Compared with Version {{ item.target.version }}
                  </div>
                </div>
                <div v-for="change in item.field_changes" :key="`${item.target.id}-${change.field}`" class="diff-table-row">
                  <div class="diff-col-field">{{ change.label }}</div>
                  <div class="diff-col-old"><span class="val-cell old-cell">{{ change.old_value || '—' }}</span></div>
                  <div class="diff-col-new"><span class="val-cell new-cell">{{ change.new_value || '—' }}</span></div>
                </div>
                <template v-if="item.component_changes?.length">
                  <div class="group-separator component-group">
                    <div class="separator-content">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
                      Component Changes
                      <span class="pill">{{ item.component_changes.length }}</span>
                    </div>
                  </div>
                  <div v-for="change in item.component_changes" :key="`${item.target.id}-comp-${change.label}`" class="diff-table-row" :class="change.change_type">
                    <div class="diff-col-field">
                      <span class="change-type-badge" :class="change.change_type" v-if="change.change_type">{{ change.change_type }}</span>
                      {{ change.label }}
                    </div>
                    <div class="diff-col-old"><span class="val-cell old-cell">{{ formatStructured(change.old_value) }}</span></div>
                    <div class="diff-col-new"><span class="val-cell new-cell">{{ formatStructured(change.new_value) }}</span></div>
                  </div>
                </template>
                <template v-if="item.workorder_changes?.length">
                  <div class="group-separator operation-group">
                    <div class="separator-content">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/></svg>
                      Operation Changes
                      <span class="pill">{{ item.workorder_changes.length }}</span>
                    </div>
                  </div>
                  <div v-for="change in item.workorder_changes" :key="`${item.target.id}-wo-${change.label}`" class="diff-table-row" :class="change.change_type">
                    <div class="diff-col-field">
                      <span class="change-type-badge" :class="change.change_type" v-if="change.change_type">{{ change.change_type }}</span>
                      {{ change.label }}
                    </div>
                    <div class="diff-col-old"><span class="val-cell old-cell">{{ formatStructured(change.old_value) }}</span></div>
                    <div class="diff-col-new"><span class="val-cell new-cell">{{ formatStructured(change.new_value) }}</span></div>
                  </div>
                </template>
                <div v-if="!item.field_changes?.length" class="diff-table-row empty">
                  <div v-if="!item.component_changes?.length && !item.workorder_changes?.length" class="empty-row">No differences found for this version.</div>
                </div>
              </template>
            </div>
          </template>

          <!-- Empty mode -->
          <div v-if="comparison.mode === 'empty'" class="empty-state">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>
            <p>{{ comparison.subtitle || 'No comparison data available yet.' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import api from '../core/api';
import { useBreadcrumbs } from '../composables/useBreadcrumbs';

const props = defineProps<{
  model: string;
  id: string;
}>();

const { push, trail } = useBreadcrumbs();
const loading = ref(true);
const error = ref('');
const comparison = ref<any>(null);

const formatStructured = (value: any) => {
  if (!value) return '—';
  if (typeof value !== 'object') return String(value);
  if (Array.isArray(value)) {
    return value.map((v: any) => typeof v === 'object' ? Object.entries(v).map(([k, val]) => `${k}: ${val}`).join(', ') : String(v)).join(' | ');
  }
  return Object.entries(value).map(([key, val]) => `${key}: ${val}`).join(' | ');
};

const updateBreadcrumbs = () => {
  if (!comparison.value) return;
  const crumbs = [...trail.value];
  if (crumbs.length > 0 && crumbs[crumbs.length - 1].label === 'Comparison') {
    return;
  }
  push({
    label: 'Comparison',
    path: `/comparison/${props.model}/${props.id}`,
    view: 'form'
  });
};

onMounted(async () => {
  loading.value = true;
  error.value = '';
  try {
    const response = await api.get(`/models/${props.model}/${props.id}/comparison`);
    comparison.value = response.data;
    updateBreadcrumbs();
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.message || 'Failed to load comparison.';
  } finally {
    loading.value = false;
  }
});

watch(comparison, () => {
    updateBreadcrumbs();
});
</script>

<style scoped lang="scss">
@use "../styles/variables" as v;

// ========== ROOT ==========
.comparison-view {
  padding: 1.5rem;
  height: 100%;
  overflow-y: auto;
  background: transparent;
  
  // Custom scrollbar for better look
  &::-webkit-scrollbar {
    width: 8px;
  }
  &::-webkit-scrollbar-track {
    background: transparent;
  }
  &::-webkit-scrollbar-thumb {
    background: v.$scrollbar-thumb;
    border-radius: 4px;
  }
  &:hover::-webkit-scrollbar-thumb {
    background: v.$scrollbar-thumb-hover;
  }
}

// ========== LOADING & ERROR STATES ==========
.comparison-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.25rem;
  padding: 6rem 2rem;
  color: v.$text-secondary;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid v.$border-color;
  border-top-color: v.$primary-color;
  border-radius: 50%;
  animation: spin 0.8s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

// ========== HEADER ==========
.comparison-header {
  margin-bottom: 2rem;
}

.header-eyebrow {
  display: block;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: v.$primary-color;
  margin-bottom: 0.5rem;
}

.header-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: v.$text-primary;
  letter-spacing: -0.03em;
  line-height: 1.1;
  margin: 0;
}

.header-subtitle {
  font-size: 1rem;
  color: v.$text-secondary;
  margin-top: 0.5rem;
  opacity: 0.8;
}

// ========== MAIN SHEET ==========
.comparison-sheet {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

// ========== SUMMARY STATS ==========
.summary-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.5rem;
  background: v.$bg-secondary;
  border: 1px solid v.$border-color;
  border-radius: v.$radius-lg;
  box-shadow: 0 1px 2px v.$shadow-color-sm;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  min-height: 90px;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px v.$shadow-color-md;
    border-color: v.$primary-color;
  }

  &.active {
    background: linear-gradient(135deg, v.$bg-secondary, v.$bg-tertiary);
    border-color: v.$primary-color;
  }
}

[data-theme="dark"] .stat-card {
  background: #161b22;
  border-color: #30363d;
  &:hover { border-color: v.$primary-color; }
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: v.$bg-tertiary;
  color: v.$text-tertiary;
  transition: all 0.2s;
  flex-shrink: 0;
}

.stat-card.active .stat-icon {
  background: rgba(v.$primary-color, 0.15);
  color: v.$primary-color;
}

.stat-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.25rem;
  min-width: 0;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 800;
  color: v.$text-primary;
  line-height: 1;
}

.stat-label {
  font-size: 0.75rem;
  color: v.$text-tertiary;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

// ========== UNIFIED DIFF TABLE ==========
.diff-master-container {
  background: v.$bg-secondary;
  border: 1px solid v.$border-color;
  border-radius: v.$radius-lg;
  box-shadow: 0 1px 3px v.$shadow-color-sm;
  overflow: hidden;
}

[data-theme="dark"] .diff-master-container {
  background: #161b22;
  border-color: #30363d;
}

.unified-diff-table {
  width: 100%;
  display: flex;
  flex-direction: column;
}

// VERSION HEADER
.version-row {
  display: grid;
  grid-template-columns: 240px 1fr 1fr;
  background: v.$bg-tertiary;
  border-bottom: 1px solid v.$border-color;
}

[data-theme="dark"] .version-row {
    background: #0d1117;
}

.info-col {
  padding: 1.5rem;
  border-right: 1px solid v.$border-color;
  display: flex;
  align-items: center;
  
  .info-label {
    font-size: 0.7rem;
    font-weight: 800;
    color: v.$text-tertiary;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }
}

.version-col {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  border-right: 1px solid v.$border-color;
  &:last-child { border-right: none; }
}

.version-hero {
  display: flex;
  align-items: center;
  gap: 0.75rem;

  .v-label {
    font-size: 0.65rem;
    font-weight: 700;
    color: v.$text-tertiary;
  }

  .v-number {
    font-size: 1.75rem;
    font-weight: 900;
    line-height: 1;
    color: v.$text-primary;
  }

  .v-status {
    font-size: 0.6rem;
    font-weight: 800;
    text-transform: uppercase;
    padding: 0.15rem 0.5rem;
    border-radius: v.$radius-pill;
    background: v.$bg-main;
    border: 1px solid v.$border-color;

    &.active { background: v.$success-bg; color: v.$success-text; border-color: transparent; }
    &.draft { background: var(--info-bg); color: var(--info-text); border-color: transparent; }
    &.archived { background: v.$bg-tertiary; color: v.$text-tertiary; border-color: v.$border-color; }
  }
}

[data-theme="dark"] .v-status.archived {
    background: #21262d;
    color: #7d8590;
    border-color: #30363d;
}

.v-details {
  font-size: 0.875rem;
  color: v.$text-secondary;
  font-weight: 500;
  opacity: 0.9;
}

// GROUP SEPARATOR
.group-separator {
  padding: 0.875rem 1.5rem;
  display: flex;
  align-items: center;
  border-bottom: 1px solid v.$border-light;

  .separator-content {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.8125rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;

    svg { opacity: 0.8; }

    .pill {
      font-size: 0.65rem;
      padding: 0.1rem 0.6rem;
      border-radius: v.$radius-pill;
    }
  }

  &.field-group { 
    background: rgba(v.$primary-color, 0.03);
    .separator-content { color: v.$primary-color; }
    .pill { background: rgba(v.$primary-color, 0.1); }
  }
  &.component-group { 
    background: rgba(v.$success-color, 0.03);
    .separator-content { color: v.$success-color; }
    .pill { background: rgba(v.$success-color, 0.1); }
  }
  &.operation-group { 
    background: rgba(v.$primary-color, 0.03);
    .separator-content { color: v.$primary-color; }
    .pill { background: rgba(v.$primary-color, 0.1); }
  }

  &.history-top {
      background: v.$bg-tertiary;
      border-top: 1px solid v.$border-color;
      padding: 1.25rem 1.5rem;
      .separator-content { color: v.$text-primary; }
  }
}

[data-theme="dark"] .group-separator {
    &.field-group { background: rgba(56, 139, 253, 0.05); }
    &.component-group { background: rgba(63, 185, 80, 0.05); }
    &.operation-group { background: rgba(99, 102, 241, 0.05); }
    &.history-top { background: #0d1117; }
}

// TABLE ROWS
.diff-table-row {
  display: grid;
  grid-template-columns: 240px 1fr 1fr;
  border-bottom: 1px solid v.$border-light;
  transition: all 0.2s;

  &:last-child { border-bottom: none; }

  &:hover {
    background: v.$bg-tertiary;
  }

  &.added { .diff-col-field { border-left: 4px solid v.$success-color; } }
  &.removed { .diff-col-field { border-left: 4px solid v.$danger-color; } }
}

[data-theme="dark"] .diff-table-row {
    border-bottom-color: #21262d;
    &:hover { background: #1c2128; }
}

.diff-col-field, .diff-col-old, .diff-col-new {
  padding: 1rem 1.5rem;
  font-size: 0.9375rem;
  border-right: 1px solid v.$border-light;
  display: flex;
  align-items: center;

  &:last-child { border-right: none; }
}

[data-theme="dark"] .diff-col-field, 
[data-theme="dark"] .diff-col-old, 
[data-theme="dark"] .diff-col-new {
    border-right-color: #21262d;
}

.diff-col-field {
  font-weight: 600;
  color: v.$text-secondary;
  background: rgba(v.$bg-tertiary, 0.3);
  gap: 0.75rem;
}

[data-theme="dark"] .diff-col-field {
    background: rgba(13, 17, 23, 0.3);
}

.old-cell { color: v.$danger-text; font-weight: 500; }
.new-cell { color: v.$success-text; font-weight: 600; }

.change-type-badge {
  font-size: 0.55rem;
  font-weight: 800;
  text-transform: uppercase;
  padding: 0.15rem 0.4rem;
  border-radius: v.$radius-sm;

  &.added { background: v.$success-bg; color: v.$success-text; }
  &.removed { background: v.$danger-bg; color: v.$danger-text; }
  &.updated { background: var(--info-bg); color: var(--info-text); }
}

// EMPTY STATE
.empty-state {
  padding: 4rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: v.$text-tertiary;
  text-align: center;
  
  .empty-row {
      font-size: 0.875rem;
      padding: 1rem;
      color: v.$text-tertiary;
  }
}
</style>
