<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="show" class="universal-search-overlay" @click.self="close">
        <div class="universal-search-container">
          <!-- Header: Search Input -->
          <div class="search-header">
            <Search class="search-icon" />
            <input 
              ref="searchInput"
              v-model="query"
              type="text"
              placeholder="Search or type a command..."
              class="search-input"
              @input="handleInput"
              @keydown.down.prevent="navigateResults(1)"
              @keydown.up.prevent="navigateResults(-1)"
              @keydown.enter.prevent="selectResult"
              @keydown.esc="close"
            />
            <div class="search-meta">
              <span class="key-hint">ESC</span>
            </div>
          </div>

          <!-- Body: Results List -->
          <div class="search-body dark-scrollbar" ref="resultsList">
            <template v-if="results.length > 0">
              <div v-for="(group, gIndex) in groupedResults" :key="group.category" class="search-group">
                <div class="group-header">{{ group.category }}</div>
                <div 
                  v-for="(result, rIndex) in group.items" 
                  :key="result.model + result.id"
                  class="search-item"
                  :class="{ active: isSelected(result) }"
                  @mouseenter="selectedIndex = getFlatIndex(gIndex, rIndex)"
                  @click="navigateTo(result)"
                >
                  <div class="item-icon">
                    <component :is="getIcon(result.icon)" class="icon-sm" />
                  </div>
                  <div class="item-info">
                    <span class="item-name">{{ result.name }}</span>
                    <span class="item-category">{{ result.category }}</span>
                  </div>
                </div>
              </div>
            </template>
            
            <div v-else-if="query.length >= 2 && !loading" class="no-results">
              <div class="no-results-icon">
                <SearchX class="icon-lg" />
              </div>
              <p>No results found for "{{ query }}"</p>
            </div>
            
            <div v-else-if="loading" class="search-loading">
              <div class="spinner"></div>
              <span>Searching...</span>
            </div>
            
            <div v-else class="search-placeholder">
              <div class="placeholder-icon">
                <Command class="icon-lg" />
              </div>
              <p>Type at least 2 characters to start searching...</p>
              
              <div v-if="history.length > 0" class="recent-searches">
                <div class="recent-header">Recent Searches</div>
                <div 
                  v-for="(item, index) in history" 
                  :key="'hist-' + index"
                  class="search-item"
                  :class="{ active: selectedIndex === index && query === '' }"
                  @mouseenter="selectedIndex = index"
                  @click="navigateTo(item)"
                >
                  <div class="item-icon">
                    <History class="icon-sm" />
                  </div>
                  <div class="item-info">
                    <span class="item-name">{{ item.name }}</span>
                    <span class="item-category">{{ item.category }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer: Keyboard Hints -->
          <div class="search-footer">
            <div class="footer-hint">
              <span class="key-badge">↑↓</span> Navigate
            </div>
            <div class="footer-hint">
              <span class="key-badge">↵</span> Select
            </div>
            <div class="footer-hint">
              <span class="key-badge">ESC</span> Close
            </div>
            <div class="footer-tag">Universal Search</div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { 
  Search, Command, History, Package, Layers, Settings, X, SearchX, ClipboardList, Box
} from 'lucide-vue-next';
import { searchService, type SearchResult } from '../../services/searchService';

const props = defineProps<{
  show: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
}>();

const router = useRouter();
const query = ref('');
const results = ref<SearchResult[]>([]);
const loading = ref(false);
const selectedIndex = ref(0);
const searchInput = ref<HTMLInputElement | null>(null);
const resultsList = ref<HTMLElement | null>(null);
const history = ref<SearchResult[]>([]);

// Group results by category
const groupedResults = computed(() => {
  const groups: Record<string, SearchResult[]> = {};
  results.value.forEach(item => {
    if (!groups[item.category]) groups[item.category] = [];
    groups[item.category].push(item);
  });
  
  return Object.keys(groups).map(category => ({
    category,
    items: groups[category]
  }));
});

// Helper to get flat index for keyboard navigation
const getFlatIndex = (gIndex: number, rIndex: number) => {
  let count = 0;
  for (let i = 0; i < gIndex; i++) {
    count += groupedResults.value[i].items.length;
  }
  return count + rIndex;
};

// Helper to check if item is selected
const isSelected = (item: SearchResult) => {
  const flatResults = groupedResults.value.flatMap(g => g.items);
  return flatResults[selectedIndex.value]?.id === item.id && 
         flatResults[selectedIndex.value]?.model === item.model;
};

// Icon mapping
const getIcon = (iconName: string) => {
  const icons: any = {
    'Package': Package,
    'Layers': Layers,
    'Settings': Settings,
    'History': History,
    'ClipboardList': ClipboardList,
    'Box': Box
  };
  return icons[iconName] || Search;
};

// Search handling
let searchTimeout: any = null;
const handleInput = () => {
  if (searchTimeout) clearTimeout(searchTimeout);
  
  if (query.value.length < 2) {
    results.value = [];
    selectedIndex.value = 0;
    return;
  }

  loading.value = true;
  searchTimeout = setTimeout(async () => {
    results.value = await searchService.query(query.value);
    loading.value = false;
    selectedIndex.value = 0;
    
    // Ensure active item is visible
    nextTick(() => {
      scrollToActive();
    });
  }, 300);
};

// Navigation
const navigateResults = (direction: number) => {
  const max = query.value === '' ? history.value.length : results.value.length;
  if (max === 0) return;
  
  selectedIndex.value = (selectedIndex.value + direction + max) % max;
  scrollToActive();
};

const scrollToActive = () => {
  if (!resultsList.value) return;
  const activeItem = resultsList.value.querySelector('.search-item.active');
  if (activeItem) {
    activeItem.scrollIntoView({ block: 'nearest' });
  }
};

const selectResult = () => {
  if (query.value === '' && history.value[selectedIndex.value]) {
    navigateTo(history.value[selectedIndex.value]);
  } else if (results.value[selectedIndex.value]) {
    navigateTo(results.value[selectedIndex.value]);
  }
};

const navigateTo = (result: SearchResult) => {
  // Save to history
  saveToHistory(result);
  
  // Close and navigate
  close();
  router.push(result.path);
};

const close = () => {
  emit('close');
  query.value = '';
  results.value = [];
  selectedIndex.value = 0;
};

// History management
const loadHistory = () => {
  const saved = localStorage.getItem('kinetic_search_history');
  if (saved) {
    try {
      history.value = JSON.parse(saved);
    } catch (e) {
      history.value = [];
    }
  }
};

const saveToHistory = (result: SearchResult) => {
  const newHistory = [result, ...history.value.filter(h => h.path !== result.path)].slice(0, 5);
  history.value = newHistory;
  localStorage.setItem('kinetic_search_history', JSON.stringify(newHistory));
};

// Watch for show to focus input
watch(() => props.show, (newVal) => {
  if (newVal) {
    nextTick(() => {
      searchInput.value?.focus();
    });
    loadHistory();
  }
});

// Global keyboard triggers
const handleGlobalKey = (e: KeyboardEvent) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    if (!props.show) emit('close'); // This logic depends on parent state
  }
};

onMounted(() => {
  window.addEventListener('keydown', handleGlobalKey);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleGlobalKey);
});
</script>

<style scoped lang="scss">
@use "../../styles/variables" as v;

.universal-search-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  z-index: 10000;
  display: flex;
  justify-content: center;
  padding-top: 10vh;
}

.universal-search-container {
  width: 100%;
  max-width: 650px;
  background: v.$white;
  border-radius: 14px;
  box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.25);
  display: flex;
  flex-direction: column;
  max-height: 70vh;
  overflow: hidden;
  border: 1px solid v.$border-light;
  animation: slideIn 0.2s ease-out;
}

@keyframes slideIn {
  from { transform: translateY(-20px) scale(0.98); opacity: 0; }
  to { transform: translateY(0) scale(1); opacity: 1; }
}

// Dark Mode Support
[data-theme="dark"] .universal-search-container {
  background: #161b22;
  border-color: #30363d;
  box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.5);
}

.search-header {
  display: flex;
  align-items: center;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid v.$border-light;
  gap: 1rem;
}

[data-theme="dark"] .search-header {
  border-bottom-color: #30363d;
}

.search-icon {
  width: 20px;
  height: 20px;
  color: v.$text-secondary;
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  font-size: 1.125rem;
  color: v.$text-primary;
  outline: none;
  
  &::placeholder {
    color: v.$text-secondary;
    opacity: 0.7;
  }
}

[data-theme="dark"] .search-input {
  color: #e6edf3;
  &::placeholder { color: #8b949e; }
}

.search-meta {
  display: flex;
  gap: 0.5rem;
}

.key-hint {
  font-size: 10px;
  font-weight: 700;
  padding: 2px 6px;
  background: v.$bg-main;
  border: 1px solid v.$border-light;
  border-radius: 4px;
  color: v.$text-secondary;
}

[data-theme="dark"] .key-hint {
  background: #21262d;
  border-color: #30363d;
  color: #8b949e;
}

.search-body {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem 0;
}

.search-group {
  margin-bottom: 0.5rem;
  
  .group-header {
    padding: 0.75rem 1.25rem 0.25rem;
    font-size: 0.75rem;
    font-weight: 700;
    color: v.$text-secondary;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
}

[data-theme="dark"] .group-header {
  color: #8b949e;
}

.search-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1.25rem;
  cursor: pointer;
  transition: all 0.15s;
  
  &.active {
    background: v.$bg-main;
    
    .item-name { color: v.$primary-color; }
  }
  
  .item-icon {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: v.$bg-main;
    border-radius: 8px;
    color: v.$text-secondary;
  }
  
  .item-info {
    display: flex;
    flex-direction: column;
    
    .item-name {
      font-size: 0.9375rem;
      font-weight: 600;
      color: v.$text-primary;
    }
    
    .item-category {
      font-size: 0.75rem;
      color: v.$text-secondary;
    }
  }
}

[data-theme="dark"] .search-item {
  &.active {
    background: #21262d;
    .item-name { color: #58a6ff; }
  }
  
  .item-icon {
    background: #21262d;
    color: #8b949e;
  }
  
  .item-info {
    .item-name { color: #e6edf3; }
    .item-category { color: #8b949e; }
  }
}

.no-results, .search-loading, .search-placeholder {
  padding: 3rem 1.25rem;
  text-align: center;
  color: v.$text-secondary;
  
  p { margin: 1rem 0 0; font-size: 0.875rem; }
  
  .icon-lg { width: 48px; height: 48px; opacity: 0.3; }
}

[data-theme="dark"] {
  .no-results, .search-loading, .search-placeholder {
    color: #8b949e;
    .icon-lg { color: #30363d; opacity: 1; }
  }
}

.search-footer {
  padding: 0.75rem 1.25rem;
  background: v.$bg-main;
  border-top: 1px solid v.$border-light;
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

[data-theme="dark"] .search-footer {
  background: #0d1117;
  border-top-color: #30363d;
}

.footer-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: v.$text-secondary;
}

.key-badge {
  background: v.$white;
  border: 1px solid v.$border-light;
  padding: 1px 4px;
  border-radius: 4px;
  font-weight: 700;
  box-shadow: 0 1px 0 rgba(0,0,0,0.1);
}

[data-theme="dark"] .key-badge {
  background: #21262d;
  border-color: #30363d;
  color: #e6edf3;
  box-shadow: 0 1px 0 rgba(255,255,255,0.05);
}

.footer-tag {
  margin-left: auto;
  font-size: 0.75rem;
  font-weight: 600;
  color: v.$text-placeholder;
  opacity: 0.5;
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.recent-searches {
    margin-top: 2rem;
    text-align: left;
    
    .recent-header {
        padding: 0 1.25rem;
        font-size: 0.75rem;
        font-weight: 700;
        color: v.$text-secondary;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
}
</style>
