<template>
  <div class="kinetic-logo" :class="layout">
    <!-- SVG Icon -->
    <svg :width="size" :height="size" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="kg1" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.8"/>
          <stop offset="100%" stop-color="#0891b2" stop-opacity="0.9"/>
        </linearGradient>
        <linearGradient id="kg2" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.7"/>
          <stop offset="100%" stop-color="#7c3aed" stop-opacity="0.8"/>
        </linearGradient>
        <linearGradient id="kg3" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.6"/>
          <stop offset="100%" stop-color="#0891b2" stop-opacity="0.7"/>
        </linearGradient>
      </defs>
      <!-- Layer 1 (bottom) -->
      <path d="M 20 65 L 50 75 L 80 65 L 50 55 Z" fill="url(#kg3)" stroke="#0891b2" stroke-width="1"/>
      <!-- Layer 2 (middle) -->
      <path d="M 20 45 L 50 55 L 80 45 L 50 35 Z" fill="url(#kg2)" stroke="#7c3aed" stroke-width="1.5"/>
      <!-- Layer 3 (top) -->
      <path d="M 20 25 L 50 35 L 80 25 L 50 15 Z" fill="url(#kg1)" stroke="#06b6d4" stroke-width="2"/>
      <!-- Connectors -->
      <line x1="50" y1="35" x2="50" y2="55" stroke="#475569" stroke-width="1" stroke-dasharray="2 2" opacity="0.5"/>
      <line x1="50" y1="55" x2="50" y2="75" stroke="#475569" stroke-width="1" stroke-dasharray="2 2" opacity="0.5"/>
      <!-- Version labels -->
      <text x="52" y="30" fill="#e2e8f0" font-size="8" font-family="monospace">v3</text>
      <text x="52" y="50" fill="#cbd5e1" font-size="7" font-family="monospace">v2</text>
      <text x="52" y="70" fill="#94a3b8" font-size="6" font-family="monospace">v1</text>
    </svg>

    <!-- Text -->
    <div v-if="showText" class="logo-text" :style="{ fontSize: textSize + 'px' }">
      <span class="logo-kinetic">KINETIC</span><span class="logo-plm">_PLM</span>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  size?: number;
  showText?: boolean;
  layout?: 'row' | 'col';
  textSize?: number;
}>(), {
  size: 40,
  showText: true,
  layout: 'row',
  textSize: 18,
});
</script>

<style scoped>
.kinetic-logo {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
}
.kinetic-logo.col {
  flex-direction: column;
  gap: 0.5rem;
}
.logo-text {
  font-family: system-ui, -apple-system, sans-serif;
  letter-spacing: 0.1em;
  line-height: 1;
}
.logo-kinetic {
  font-weight: 600;
  color: #e2e8f0;
}
.logo-plm {
  font-weight: 300;
  color: #64748b;
}
</style>
