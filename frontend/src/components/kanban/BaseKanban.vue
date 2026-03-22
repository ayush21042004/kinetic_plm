<template>
  <div class="base-kanban" :class="{ 'loading': loading }">
    <!-- Action Bar -->
    <div class="action-bar">
      <div class="action-bar-left">
        <button class="btn btn-primary" @click="$emit('create')">
          <span>New</span>
        </button>
      </div>
      
      <div class="action-bar-center">
        <AdvancedSearchBar
          :metadata="metadata"
          :search="currentSearch"
          :filters="activeFilters"
          :group-by="activeGroupBy"
          @search="(d) => $emit('search', d)"
          @filter="(f) => $emit('filter', f)"
          @group-by="(g) => $emit('group-by', g)"
          @clear="$emit('clear-all')"
        />
      </div>
 
      <div class="action-bar-right">
        <!-- View Toggle Buttons -->
        <div class="view-toggle-buttons">
          <button 
            class="view-toggle-btn" 
            :class="{ active: viewType === 'list' }"
            @click="$emit('update:view-type', 'list')"
            title="List View"
          >
            <LayoutList class="icon-xs" />
          </button>
          <button 
            class="view-toggle-btn" 
            :class="{ active: viewType === 'kanban' }"
            @click="$emit('update:view-type', 'kanban')"
            title="Kanban View"
          >
            <LayoutGrid class="icon-xs" />
          </button>
        </div>

        <div class="pager-wrapper" v-if="totalCount">
          <div class="nav-arrows">
            <button class="nav-arrow" @click="$emit('paginate', Math.max(0, offset - limit))" :disabled="offset === 0">
              <ChevronLeft class="icon-sm" />
            </button>
            <button class="nav-arrow" @click="$emit('paginate', offset + limit)" :disabled="offset + limit >= totalCount">
              <ChevronRight class="icon-sm" />
            </button>
          </div>
          <span class="pager-info">{{ pageRange }} / {{ totalCount }}</span>
        </div>
      </div>
    </div>

    <!-- Kanban Container -->
    <div v-if="loading && items.length === 0" class="kanban-skeleton">
      <div v-for="i in 3" :key="i" class="kanban-column-skeleton">
        <div class="column-header-skeleton"></div>
        <div v-for="j in 3" :key="j" class="kanban-card-skeleton"></div>
      </div>
    </div>
    
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
    </div>

    <div v-else class="kanban-container dark-scrollbar" :class="{ 'is-grouped': hasGrouping, 'is-flat': !hasGrouping }">
      <!-- Grouped View (Columns) -->
      <template v-if="hasGrouping">
        <div v-for="group in groupedResults" :key="group.value" class="kanban-column">
          <header class="column-header">
            <div class="column-title-group">
              <span class="column-dot" :class="getGroupColor(group)"></span>
              <h3 class="column-title">{{ formatGroupHeader(group) }}</h3>
              <span class="column-count">{{ group.count }}</span>
            </div>
          </header>

          <div class="column-cards dark-scrollbar">
            <div 
              v-for="item in group.items" 
              :key="item.id" 
              class="kanban-card"
              @click="$emit('view', item.id)"
            >
              <div class="card-edge" :class="getGroupColor(group)"></div>
              <div class="card-content">
                <!-- Card Header -->
                <div class="card-header">
                  <span class="card-name">{{ item[nameField] || 'Unnamed' }}</span>
                  <span v-if="item.id" class="card-id">#{{ item.id }}</span>
                </div>

                <!-- Card Body (Model Specific Fields) -->
                <div class="card-body">
                  <div v-for="field in cardFields" :key="field.key" class="card-field">
                    <span class="field-label">{{ field.label }}:</span>
                    <span class="field-value">{{ formatValue(item[field.key], field.type, field) }}</span>
                  </div>
                </div>

                <!-- Card Footer (Meta/Avatar) -->
                <div v-if="hasFooterMeta(item)" class="card-footer">
                  <div class="card-meta">
                    <span v-if="item.created_at" class="card-date">{{ formatDate(item.created_at) }}</span>
                  </div>
                  <div v-if="item.user_id || item.initiator" class="card-user">
                    <div class="user-avatar-mini">{{ (item.user_name || item.initiator || 'U').charAt(0) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>

      <!-- Flat View (No Group By) -->
      <template v-else-if="items.length > 0">
        <div
          v-for="item in items"
          :key="item.id"
          class="kanban-card kanban-card-flat"
          @click="$emit('view', item.id)"
        >
          <div class="card-edge color-default"></div>
          <div class="card-content">
            <div class="card-header">
              <span class="card-name">{{ item[nameField] || 'Unnamed' }}</span>
              <span v-if="item.id" class="card-id">#{{ item.id }}</span>
            </div>

            <div class="card-body">
              <div v-for="field in cardFields" :key="field.key" class="card-field">
                <span class="field-label">{{ field.label }}:</span>
                <span class="field-value">{{ formatValue(item[field.key], field.type, field) }}</span>
              </div>
            </div>

            <div v-if="hasFooterMeta(item)" class="card-footer">
              <div class="card-meta">
                <span v-if="item.created_at" class="card-date">{{ formatDate(item.created_at) }}</span>
              </div>
              <div v-if="item.user_id || item.initiator" class="card-user">
                <div class="user-avatar-mini">{{ (item.user_name || item.initiator || 'U').charAt(0) }}</div>
              </div>
            </div>
          </div>
        </div>
      </template>

      <div v-else class="empty-state">
        <div class="empty-content">
          <LayoutGrid :size="48" class="empty-icon" />
          <h3>No records found</h3>
          <p>Try adjusting your search or filters.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { LayoutGrid, LayoutList, ChevronLeft, ChevronRight } from 'lucide-vue-next';
import { formatDate, formatDateTime } from '../../utils/dateUtils';
import AdvancedSearchBar from '../list/AdvancedSearchBar.vue';

const props = defineProps<{
  items: any[];
  totalCount: number;
  offset: number;
  limit: number;
  metadata: any;
  loading: boolean;
  error?: string | null;
  groupedResults?: any[];
  activeGroupBy?: string;
  modelName?: string;
  viewType?: 'list' | 'kanban';
  currentSearch?: string;
  activeFilters?: any[];
}>();

const emit = defineEmits(['view', 'create', 'search', 'filter', 'group-by', 'clear-all', 'paginate', 'update:view-type']);

const pageRange = computed(() => {
    const start = props.offset + 1;
    const end = Math.min(props.offset + props.limit, props.totalCount);
    return `${start}-${end}`;
});

const hasGrouping = computed(() => !!props.activeGroupBy && !!props.groupedResults?.length);

const allFields = computed(() => props.metadata.fields || {});
const nameField = computed(() => props.metadata.name_field || 'name');

// Define which fields to show in the card based on the model
const cardFields = computed(() => {
  const fields = [];
  const model = props.modelName;
  const metaFields = props.metadata.fields || {};

  if (model === 'plm.eco') {
    if (metaFields.type) fields.push({ key: 'type', label: 'Type', type: 'selection' });
    if (metaFields.stage_id) fields.push({ key: 'stage_id', label: 'Stage', type: 'many2one' });
    if (metaFields.product_id) fields.push({ key: 'product_id', label: 'Product', type: 'many2one' });
    if (metaFields.bom_id) fields.push({ key: 'bom_id', label: 'Target BoM', type: 'many2one' });
    if (metaFields.initiated_by_id) fields.push({ key: 'initiated_by_id', label: 'Initiated By', type: 'many2one' });
  } else if (model === 'product.version') {
    if (metaFields.version) fields.push({ key: 'version', label: 'Ver', type: 'integer' });
    if (metaFields.default_code) fields.push({ key: 'default_code', label: 'Ref', type: 'char' });
    if (metaFields.state) fields.push({ key: 'state', label: 'State', type: 'selection' });
    if (metaFields.sale_price) fields.push({ key: 'sale_price', label: 'Price', type: 'integer' });
  } else if (model === 'mrp.bom') {
    if (metaFields.version) fields.push({ key: 'version', label: 'Ver', type: 'integer' });
    if (metaFields.product_version_id) fields.push({ key: 'product_version_id', label: 'Product', type: 'many2one' });
    if (metaFields.state) fields.push({ key: 'state', label: 'State', type: 'selection' });
    if (metaFields.eco_id) fields.push({ key: 'eco_id', label: 'Source ECO', type: 'many2one' });
  } else {
    // Generic first 2 fields
    const keys = Object.keys(metaFields).filter(k => k !== nameField.value && k !== 'id' && metaFields[k].type !== 'one2many').slice(0, 2);
    for (const k of keys) {
      fields.push({ key: k, label: metaFields[k].label, type: metaFields[k].type });
    }
  }
  return fields;
});

const formatValue = (value: any, type: string, field: any) => {
  if (value === null || value === undefined) return '-';
  if (type === 'many2one') {
    return value.display_name || value.name || value.id || value;
  }
  if (type === 'selection') {
    const options = allFields.value[field.key]?.options || {};
    return (options[value]?.label || options[value] || value);
  }
  if (type === 'date') return formatDate(value);
  if (type === 'datetime') return formatDateTime(value);
  return value;
};

const formatGroupHeader = (group: any) => {
    // group.value is the label, group.group_value is the raw ID/Selection key
    return group.value || 'Undefined';
};

const hasFooterMeta = (item: any) => {
  return !!(item?.created_at || item?.user_id || item?.initiator);
};

const getGroupColor = (group: any) => {
  const val = String(group.group_value || group.value || '').toLowerCase();
  if (val.includes('draft') || val.includes('new')) return 'color-info';
  if (val.includes('active') || val.includes('approve') || val.includes('valid')) return 'color-success';
  if (val.includes('archive') || val.includes('close') || val.includes('cancel')) return 'color-danger';
  if (val.includes('warning') || val.includes('process')) return 'color-warning';
  return 'color-default';
};
</script>

<style lang="scss" scoped>
@use "../../styles/variables" as v;

.base-kanban {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  background: v.$bg-main;
  overflow: hidden;
}

/* Action Bar Styles (Matching BaseList) */
.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.5rem;
  background: v.$bg-secondary;
  border-bottom: 1px solid v.$border-color;
  gap: 1.5rem;
  flex-shrink: 0;
}

.action-bar-left, .action-bar-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.action-bar-center {
  flex: 1;
  max-width: 600px;
}

.view-toggle-buttons {
  display: flex;
  background: v.$bg-tertiary;
  padding: 0.25rem;
  border-radius: 0.5rem;
  border: 1px solid v.$border-color;
}

.view-toggle-btn {
  background: transparent;
  border: 1px solid transparent;
  padding: 0.375rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: v.$text-secondary;
  border-radius: 0.375rem;
  transition: all 0.2s;

  &:hover {
    color: v.$text-primary;
    background: rgba(v.$primary-color, 0.1);
  }

  &.active {
    background: color-mix(in srgb, v.$primary-color 16%, v.$bg-secondary);
    color: v.$primary-color;
    border: 1px solid color-mix(in srgb, v.$primary-color 45%, v.$border-color);
    box-shadow: 0 0 0 1px color-mix(in srgb, v.$primary-color 12%, transparent);
  }
}

.pager-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding-left: 1rem;
  border-left: 1px solid v.$border-color;
}

.nav-arrows {
  display: flex;
  gap: 0.25rem;
}

.nav-arrow {
  background: none;
  border: 1px solid v.$border-color;
  border-radius: 4px;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  cursor: pointer;
  color: v.$text-primary;
  transition: all 0.2s;

  &:hover:not(:disabled) {
    background: v.$bg-tertiary;
    border-color: v.$text-secondary;
  }

  &:disabled {
    opacity: 0.5;
    cursor: default;
  }
}

.pager-info {
  font-size: 0.8125rem;
  color: v.$text-secondary;
  white-space: nowrap;
}

.kanban-container {
  flex: 1;
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
  overflow-x: auto;
  overflow-y: hidden;
  align-items: flex-start;
  min-height: 200px;
  min-width: 0;
  min-height: 0;
}

.kanban-container.is-flat {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  grid-auto-rows: max-content;
  align-content: start;
  align-items: start;
  overflow-x: hidden;
  overflow-y: auto;
}

.kanban-column {
  flex: 0 0 320px;
  display: flex;
  flex-direction: column;
  align-self: stretch;
  min-height: 0;
  background: rgba(v.$bg-secondary, 0.4);
  backdrop-filter: blur(8px);
  border-radius: 1rem;
  border: 1px solid v.$border-color;
  transition: all 0.3s ease;

  &:hover {
    background: rgba(v.$bg-secondary, 0.6);
    border-color: rgba(v.$primary-color, 0.3);
  }
}

.column-header {
  flex-shrink: 0;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid v.$border-color;
  
  .column-title-group {
    display: flex;
    align-items: center;
    gap: 0.75rem;

    .column-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: v.$text-secondary;

      &.color-info { background: v.$info-color; }
      &.color-success { background: v.$success-color; }
      &.color-danger { background: v.$danger-color; }
      &.color-warning { background: v.$warning-color; }
    }

    .column-title {
      font-size: 0.9375rem;
      font-weight: 600;
      color: v.$text-primary;
      margin: 0;
      flex: 1;
    }

    .column-count {
      font-size: 0.75rem;
      font-weight: 500;
      color: v.$text-secondary;
      background: v.$bg-tertiary;
      padding: 0.125rem 0.5rem;
      border-radius: 1rem;
    }
  }
}

.column-cards {
  flex: 1;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow-y: auto;
  min-height: 100px;
  min-width: 0;
  min-height: 0;
}

.kanban-card {
  background: v.$bg-secondary;
  border-radius: 0.75rem;
  border: 1px solid v.$border-color;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 3px v.$shadow-light;

  &:hover {
    transform: translateY(-2px);
    box-shadow: v.$shadow-md;
    border-color: v.$primary-color;
  }

  .card-edge {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: v.$border-color;

    &.color-info { background: v.$info-color; }
    &.color-success { background: v.$success-color; }
    &.color-danger { background: v.$danger-color; }
    &.color-warning { background: v.$warning-color; }
    &.color-default { background: v.$primary-color; }
  }

  .card-content {
    padding: 1rem;
    padding-left: 1.25rem;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.75rem;
    gap: 0.5rem;

    .card-name {
      font-weight: 600;
      font-size: 0.9375rem;
      color: v.$text-primary;
      line-height: 1.3;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .card-id {
      font-size: 0.75rem;
      color: v.$text-secondary;
      font-family: monospace;
      white-space: nowrap;
    }
  }

  .card-body {
    display: flex;
    flex-direction: column;
    gap: 0.375rem;

    .card-field {
      display: flex;
      font-size: 0.8125rem;
      gap: 0.5rem;

      .field-label {
        color: v.$text-secondary;
        font-weight: 500;
      }

      .field-value {
        color: v.$text-primary;
        white-space: normal;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1.35;
      }
    }
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
    padding-top: 0.75rem;
    border-top: 1px dashed v.$border-color;

    .card-date {
      font-size: 0.75rem;
      color: v.$text-secondary;
    }

    .user-avatar-mini {
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: v.$primary-color;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.75rem;
      font-weight: 600;
      border: 2px solid v.$bg-secondary;
      box-shadow: 0 0 0 1px v.$border-color;
    }
  }
}

.kanban-card-flat {
  display: block;
  align-self: start;
  min-width: 0;
  height: max-content;
}

.empty-state {
  width: 100%;
  min-height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px dashed v.$border-color;
  border-radius: 1rem;
  background: rgba(v.$bg-secondary, 0.5);
}

.empty-content {
  text-align: center;
  color: v.$text-secondary;

  h3 {
    margin: 0.75rem 0 0.25rem;
    color: v.$text-primary;
    font-size: 1rem;
  }

  p {
    margin: 0;
    font-size: 0.875rem;
  }
}

.empty-icon {
  color: v.$text-secondary;
  opacity: 0.8;
}

// Skeletons
.kanban-skeleton {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
}

.kanban-column-skeleton {
  flex: 0 0 320px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.column-header-skeleton {
  height: 48px;
  background: v.$bg-secondary;
  border-radius: 0.75rem;
  animation: pulse 2s infinite;
}

.kanban-card-skeleton {
  height: 120px;
  background: white;
  border-radius: 0.75rem;
  border: 1px solid v.$border-color;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 0.8; }
  100% { opacity: 0.6; }
}

.empty-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem;

  .empty-content {
    text-align: center;
    color: v.$text-secondary;

    .empty-icon {
      margin-bottom: 1rem;
      opacity: 0.2;
    }

    h3 {
      font-size: 1.25rem;
      color: v.$text-primary;
      margin-bottom: 0.5rem;
    }
  }
}
</style>
