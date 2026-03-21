<template>
  <div class="landing-wrap">
    <!-- Grid Overlay -->
    <div class="grid-overlay"></div>

    <!-- Navigation -->
    <nav class="top-nav">
      <div class="nav-inner">
        <KineticLogo :size="32" :text-size="16" />
        <div class="nav-links">
          <a href="#features">CAPABILITIES</a>
          <a href="#workflow">WORKFLOW</a>
          <a href="#traceability">TRACEABILITY</a>
          <a href="#roles">ROLES</a>
        </div>
        <div class="nav-actions">
          <button class="btn-ghost" @click="$router.push('/login')">LOG_IN</button>
          <button class="btn-primary" @click="$router.push('/signup')">PROVISION_ACCOUNT</button>
        </div>
      </div>
    </nav>

    <!-- Hero -->
    <section class="hero">
      <div class="hero-inner">
        <div class="hero-text">
          <div class="status-badge">
            <span class="pulse-dot"></span>
            <span>System Status: Optimal</span>
          </div>
          <h1>
            Control every engineering change with
            <span class="text-accent">versioned precision.</span>
          </h1>
          <p class="hero-sub">
            Manage Products, BoMs, ECOs, approvals, and traceability without direct master-data edits.
            The clinical core for industrial hardware development.
          </p>
          <div class="hero-ctas">
            <button class="btn-primary btn-lg" @click="$router.push('/signup')">Initialize Protocol</button>
            <button class="btn-outline btn-lg">View technical spec</button>
          </div>
        </div>

        <!-- Dashboard Preview Panel -->
        <div class="hero-visual">
          <div class="glass-panel">
            <div class="panel-header">
              <div class="panel-title">
                <span class="material-symbols-outlined">settings_input_component</span>
                <span>ECO-2024-089 // PROPULSION_MODULE</span>
              </div>
              <div class="panel-dots">
                <span class="dot-red"></span>
                <span class="dot-yellow"></span>
                <span class="dot-green"></span>
              </div>
            </div>
            <div class="panel-body">
              <div class="progress-track">
                <div class="track-seg active"></div>
                <div class="track-seg active"></div>
                <div class="track-seg dim"></div>
                <div class="track-seg faint"></div>
              </div>
              <div class="eco-card">
                <div class="eco-meta">
                  <div>
                    <div class="meta-label">Current Version</div>
                    <div class="meta-value">v4.2.1-stable</div>
                  </div>
                  <div class="badge-approved">Approved</div>
                </div>
                <div class="eco-lines">
                  <div class="eco-line">
                    <span>Line Item 402: Cooling Shroud</span>
                    <span class="val-removed">- 2.4mm</span>
                  </div>
                  <div class="eco-line">
                    <span>Line Item 405: Intake Valve</span>
                    <span class="val-added">+ Grade-5 Titanium</span>
                  </div>
                  <div class="eco-line">
                    <span>Line Item 412: Thermal Paste</span>
                    <span class="val-modified">MODIFIED</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="hero-glow-1"></div>
          <div class="hero-glow-2"></div>
        </div>
      </div>
    </section>

    <!-- Features Bento Grid -->
    <section id="features" class="features">
      <div class="section-inner">
        <div class="section-head">
          <h2>Core Technical Capabilities</h2>
          <div class="head-bar"></div>
        </div>
        <div class="bento-grid">
          <div class="bento-card" v-for="feat in features" :key="feat.title">
            <span class="material-symbols-outlined feat-icon">{{ feat.icon }}</span>
            <h3>{{ feat.title }}</h3>
            <p>{{ feat.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Workflow -->
    <section id="workflow" class="workflow">
      <div class="section-inner">
        <div class="workflow-layout">
          <div class="workflow-text">
            <h2>The Immutable <span class="text-accent">Workflow</span></h2>
            <p>KINETIC_PLM enforces a non-linear but highly controlled path from concept to production release.</p>
          </div>
          <div class="workflow-steps">
            <div class="step-connector"></div>
            <div class="step" v-for="step in workflowSteps" :key="step.label" :class="{ 'step-active': step.active, 'step-final': step.final }">
              <div class="step-num">{{ step.num }}</div>
              <div class="step-label">{{ step.label }}</div>
              <div class="step-dots" v-if="step.dots">
                <span v-for="n in 3" :key="n" :class="n <= step.dots ? 'dot-filled' : 'dot-empty'"></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Traceability -->
    <section id="traceability" class="traceability">
      <div class="section-inner">
        <div class="trace-layout">
          <div class="trace-text">
            <h2>Traceability &amp; Diff-Logic</h2>
            <p>Instant visual verification of engineering changes. Identify discrepancies between revisions with microscopic detail.</p>
            <div class="trace-features">
              <div class="trace-feat active">
                <span class="material-symbols-outlined">data_thresholding</span>
                <div>
                  <div class="tf-title">Automated Diff Generation</div>
                  <div class="tf-sub">Compare BOMs and CAD metadata instantly.</div>
                </div>
              </div>
              <div class="trace-feat">
                <span class="material-symbols-outlined">history</span>
                <div>
                  <div class="tf-title">Universal History Timeline</div>
                  <div class="tf-sub">Every action, timestamped and user-bound.</div>
                </div>
              </div>
            </div>
          </div>
          <div class="diff-panel">
            <div class="diff-header">
              <span>COMPARISON_ENGINE: v2.4.0 vs v2.5.0</span>
              <span class="diff-rate">MATCH_RATE: 94.2%</span>
            </div>
            <div class="diff-body">
              <div class="diff-line neutral">
                <span class="ln">102</span>
                <span>PART_ID: AX-901 // MATERIAL: ALUMINUM_6061</span>
              </div>
              <div class="diff-line removed">
                <span class="ln">103</span>
                <span>- TOLERANCE: 0.005mm // QTY: 4</span>
              </div>
              <div class="diff-line added">
                <span class="ln">103</span>
                <span>+ TOLERANCE: 0.002mm // QTY: 4 // NOTES: PRECISION_INCREASE</span>
              </div>
              <div class="diff-line neutral">
                <span class="ln">104</span>
                <span>FASTENER: M4_HEX_SCREW // COATING: NONE</span>
              </div>
              <div class="diff-line added">
                <span class="ln">105</span>
                <span>+ COATING: ZINC_PLATE // REF: ISO-4042</span>
              </div>
            </div>
            <div class="diff-footer">
              <span class="diff-author">Modified by J. ARCHER // 2024-05-12 14:22:01</span>
              <button class="btn-text">Accept Change</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Roles -->
    <section id="roles" class="roles">
      <div class="section-inner">
        <h2 class="roles-title">Ecosystem Roles</h2>
        <div class="roles-grid">
          <div class="role-card" v-for="role in roles" :key="role.code" :style="{ '--role-color': role.color }">
            <div class="role-code">{{ role.code }}</div>
            <h3>{{ role.name }}</h3>
            <ul>
              <li v-for="perm in role.perms" :key="perm">
                <span class="role-slash">/</span> {{ perm }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta-section">
      <div class="cta-glow"></div>
      <div class="cta-inner">
        <h2>Safe, auditable engineering change control</h2>
        <p>Ready to deploy the kinetic core of your hardware development lifecycle?</p>
        <div class="cta-btns">
          <button class="btn-primary btn-lg" @click="$router.push('/signup')">Deploy Now</button>
          <button class="btn-outline btn-lg">Request Demo</button>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="site-footer">
      <div class="footer-inner">
        <div class="footer-brand">
          <KineticLogo :size="24" :text-size="14" />
          <p>©2024 KINETIC_PLM // SECURE_INDUSTRIAL_CORE</p>
        </div>
        <div class="footer-links">
          <a href="#">LEGAL_DOCUMENTATION</a>
          <a href="#">SYSTEM_STATUS</a>
          <a href="#">API_REF</a>
          <a href="#">ENCRYPTION_STANDARDS</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import KineticLogo from '@/components/KineticLogo.vue';
const features = [
  { icon: 'schema', title: 'Controlled ECO Workflows', desc: 'Multi-stage engineering change orders with mandatory justification and impact analysis.' },
  { icon: 'history_toggle_off', title: 'Product Versioning', desc: 'Granular version control for physical assets, mirroring software-grade branch logic.' },
  { icon: 'reorder', title: 'BoM Version Control', desc: 'Bill of Materials management with automated diffing and cross-reference validation.' },
  { icon: 'verified_user', title: 'Approval Stages', desc: 'Customizable signature chains requiring cryptographic verification for each gate.' },
  { icon: 'receipt_long', title: 'Audit Trail', desc: 'Immutable logs of every modification, login, and approval for compliance adherence.' },
  { icon: 'admin_panel_settings', title: 'RBAC Precision', desc: 'Hierarchical permissions ensuring only authorized personnel can initiate or approve changes.' },
];

const workflowSteps = [
  { num: 'STEP_01', label: 'New ECO', dots: 1 },
  { num: 'STEP_02', label: 'Review', dots: 2 },
  { num: 'STEP_03', label: 'Approval', dots: 3, active: true },
  { num: 'STEP_04', label: 'Version Update', dots: 0 },
  { num: 'FINAL', label: 'Active Release', final: true },
];

const roles = [
  { code: 'ENG_USER', name: 'Engineering', color: '#a4e6ff', perms: ['Create ECO Drafts', 'Upload CAD Metadata', 'Version BoM Items'] },
  { code: 'APP_GATE', name: 'Approver', color: '#7cecff', perms: ['Review Change Impact', 'Sign-off Releases', 'Reject with Logic'] },
  { code: 'OPS_CORE', name: 'Operations', color: '#c8c6c5', perms: ['View Active Releases', 'Export BOM for ERP', 'Track Part Usage'] },
  { code: 'SYS_ADM', name: 'Admin', color: '#859399', perms: ['Configure Workflows', 'User Management', 'Audit Log Access'] },
];
</script>

<style scoped>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

.material-symbols-outlined {
  font-family: 'Material Symbols Outlined';
  font-variation-settings: 'FILL' 0, 'wght' 300, 'GRAD' 0, 'opsz' 24;
  font-style: normal;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  white-space: nowrap;
  word-wrap: normal;
  direction: ltr;
  -webkit-font-smoothing: antialiased;
}

/* ── Base ── */
* { box-sizing: border-box; margin: 0; padding: 0; }

.landing-wrap {
  min-height: 100vh;
  background: #131313;
  color: #e5e2e1;
  font-family: 'Inter', sans-serif;
  overflow-x: hidden;
  position: relative;
}

.grid-overlay {
  position: fixed;
  inset: 0;
  background-image: radial-gradient(#00d1ff 0.5px, transparent 0.5px);
  background-size: 24px 24px;
  opacity: 0.05;
  pointer-events: none;
  z-index: 0;
}

.text-accent { color: #a4e6ff; }

/* ── Nav ── */
.top-nav {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(19, 19, 19, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 209, 255, 0.1);
}
.nav-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1440px;
  margin: 0 auto;
  padding: 1rem 1.5rem;
}
.nav-brand {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.05em;
  color: #a4e6ff;
  text-shadow: 0 0 8px rgba(0, 209, 255, 0.3);
}
.nav-links {
  display: flex;
  gap: 2rem;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
}
.nav-links a {
  color: #859399;
  text-decoration: none;
  transition: color 0.2s;
}
.nav-links a:hover { color: #a4e6ff; }
.nav-actions { display: flex; gap: 1rem; align-items: center; }

@media (max-width: 768px) {
  .nav-links { display: none; }
}

/* ── Buttons ── */
.btn-ghost {
  background: none;
  border: none;
  color: #859399;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  cursor: pointer;
  transition: color 0.2s;
}
.btn-ghost:hover { color: #a4e6ff; }

.btn-primary {
  background: #00d1ff;
  color: #003543;
  border: none;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 0.5rem 1.25rem;
  cursor: pointer;
  box-shadow: 0 0 20px rgba(0, 209, 255, 0.2);
  transition: transform 0.15s, box-shadow 0.15s;
}
.btn-primary:hover {
  transform: scale(1.02);
  box-shadow: 0 0 30px rgba(0, 209, 255, 0.35);
}
.btn-primary.btn-lg { padding: 1rem 2rem; font-size: 0.8rem; }

.btn-outline {
  background: none;
  border: 1px solid rgba(133, 147, 153, 0.3);
  color: #e5e2e1;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 0.5rem 1.25rem;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-outline:hover { background: #2a2a2a; }
.btn-outline.btn-lg { padding: 1rem 2rem; font-size: 0.8rem; }

.btn-text {
  background: none;
  border: none;
  color: #a4e6ff;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  cursor: pointer;
  transition: text-decoration 0.2s;
}
.btn-text:hover { text-decoration: underline; }

/* ── Section Shared ── */
.section-inner {
  max-width: 1440px;
  margin: 0 auto;
  padding: 6rem 1.5rem;
}
.section-head { margin-bottom: 4rem; }
.section-head h2 {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: -0.02em;
  margin-bottom: 0.5rem;
}
.head-bar { width: 5rem; height: 4px; background: #a4e6ff; }

/* ── Hero ── */
.hero { position: relative; z-index: 1; }
.hero-inner {
  max-width: 1440px;
  margin: 0 auto;
  padding: 6rem 1.5rem 3rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}
@media (max-width: 1024px) {
  .hero-inner { grid-template-columns: 1fr; }
  .hero-visual { display: none; }
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  background: #353534;
  border: 1px solid rgba(60, 73, 78, 0.2);
  margin-bottom: 1.5rem;
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #a4e6ff;
}
.pulse-dot {
  width: 8px;
  height: 8px;
  background: #a4e6ff;
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

.hero-text h1 {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(2.5rem, 5vw, 4.5rem);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.03em;
  margin-bottom: 1.5rem;
}
.hero-sub {
  color: #bbc9cf;
  font-size: 1.125rem;
  line-height: 1.6;
  max-width: 36rem;
  margin-bottom: 2.5rem;
}
.hero-ctas { display: flex; gap: 1rem; flex-wrap: wrap; }

/* Hero Visual */
.hero-visual { position: relative; }
.glass-panel {
  backdrop-filter: blur(20px);
  background: rgba(0, 209, 255, 0.05);
  border: 1px solid rgba(164, 230, 255, 0.2);
  padding: 1rem;
  position: relative;
  z-index: 1;
  box-shadow: 0 0 20px rgba(0, 209, 255, 0.2);
}
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid rgba(60, 73, 78, 0.2);
}
.panel-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #bbc9cf;
}
.panel-title .material-symbols-outlined { font-size: 1rem; color: #a4e6ff; }
.panel-dots { display: flex; gap: 4px; }
.dot-red { width: 8px; height: 8px; background: #ffb4ab; }
.dot-yellow { width: 8px; height: 8px; background: #7cecff; }
.dot-green { width: 8px; height: 8px; background: #a4e6ff; }

.progress-track { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; margin-bottom: 1rem; }
.track-seg { height: 4px; }
.track-seg.active { background: #a4e6ff; }
.track-seg.dim { background: rgba(164, 230, 255, 0.3); }
.track-seg.faint { background: rgba(164, 230, 255, 0.1); }

.eco-card {
  background: #0e0e0e;
  padding: 1rem;
  border: 1px solid rgba(60, 73, 78, 0.1);
}
.eco-meta {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}
.meta-label { font-size: 0.5625rem; text-transform: uppercase; letter-spacing: 0.05em; color: #859399; margin-bottom: 0.25rem; }
.meta-value { font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; color: #e5e2e1; }
.badge-approved {
  background: rgba(0, 211, 235, 0.15);
  color: #7cecff;
  padding: 0.25rem 0.5rem;
  font-size: 0.5625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.eco-lines { display: flex; flex-direction: column; gap: 0.5rem; }
.eco-line {
  display: flex;
  justify-content: space-between;
  font-size: 0.625rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(60, 73, 78, 0.05);
  color: #bbc9cf;
}
.eco-line:last-child { border-bottom: none; }
.val-removed { color: #ffb4ab; font-family: monospace; }
.val-added { color: #7cecff; font-family: monospace; }
.val-modified { color: #a4e6ff; font-family: monospace; }

.hero-glow-1 {
  position: absolute;
  top: -2.5rem;
  right: -2.5rem;
  width: 16rem;
  height: 16rem;
  background: rgba(164, 230, 255, 0.05);
  filter: blur(100px);
  border-radius: 50%;
}
.hero-glow-2 {
  position: absolute;
  bottom: -5rem;
  left: -5rem;
  width: 20rem;
  height: 20rem;
  background: rgba(124, 236, 255, 0.05);
  filter: blur(120px);
  border-radius: 50%;
}

/* ── Features ── */
.features { background: #131313; }
.bento-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
}
@media (max-width: 900px) { .bento-grid { grid-template-columns: 1fr 1fr; } }
@media (max-width: 600px) { .bento-grid { grid-template-columns: 1fr; } }

.bento-card {
  padding: 2rem;
  border: 1px solid rgba(60, 73, 78, 0.1);
  transition: border-color 0.2s;
  cursor: default;
}
.bento-card:nth-child(odd) { background: #1c1b1b; }
.bento-card:nth-child(even) { background: #201f1f; }
.bento-card:hover { border-color: rgba(164, 230, 255, 0.3); }

.feat-icon {
  display: block;
  color: #a4e6ff;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  transition: transform 0.2s;
}
.bento-card:hover .feat-icon { transform: scale(1.1); }

.bento-card h3 {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
}
.bento-card p { color: #bbc9cf; font-size: 0.875rem; line-height: 1.6; }

/* ── Workflow ── */
.workflow { background: #0e0e0e; }
.workflow-layout {
  display: flex;
  gap: 3rem;
  align-items: center;
}
@media (max-width: 768px) { .workflow-layout { flex-direction: column; } }

.workflow-text { flex: 0 0 30%; }
.workflow-text h2 {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 2.5rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: -0.02em;
  margin-bottom: 1.5rem;
  line-height: 1.1;
}
.workflow-text p { color: #bbc9cf; line-height: 1.6; }

.workflow-steps {
  flex: 1;
  position: relative;
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}
.step-connector {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 1px;
  background: rgba(60, 73, 78, 0.2);
}
@media (max-width: 768px) { .step-connector { display: none; } }

.step {
  position: relative;
  z-index: 1;
  background: #131313;
  border: 1px solid rgba(60, 73, 78, 0.2);
  padding: 1.5rem;
  flex: 1;
  min-width: 100px;
}
.step.step-active {
  border-color: #a4e6ff;
  box-shadow: 0 0 15px rgba(0, 209, 255, 0.1);
}
.step.step-final {
  background: rgba(0, 211, 235, 0.15);
  color: #e5e2e1;
  border-color: transparent;
}

.step-num {
  font-size: 0.625rem;
  font-weight: 700;
  color: #a4e6ff;
  letter-spacing: 0.2em;
  margin-bottom: 0.5rem;
}
.step.step-final .step-num { color: #e5e2e1; }
.step-label {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
.step-dots { display: flex; gap: 4px; margin-top: 1rem; }
.dot-filled { width: 6px; height: 6px; background: #a4e6ff; }
.dot-empty { width: 6px; height: 6px; background: rgba(60, 73, 78, 0.2); }

/* ── Traceability ── */
.traceability { background: #131313; }
.trace-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: start;
}
@media (max-width: 900px) { .trace-layout { grid-template-columns: 1fr; } }

.trace-text h2 {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: -0.02em;
  margin-bottom: 1.5rem;
}
.trace-text > p { color: #bbc9cf; font-size: 1.125rem; margin-bottom: 2rem; line-height: 1.6; }

.trace-features { display: flex; flex-direction: column; gap: 1rem; }
.trace-feat {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #1c1b1b;
  border-left: 2px solid rgba(60, 73, 78, 0.3);
}
.trace-feat.active { border-left-color: #a4e6ff; }
.trace-feat .material-symbols-outlined { color: #859399; }
.trace-feat.active .material-symbols-outlined { color: #a4e6ff; }
.tf-title { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #e5e2e1; margin-bottom: 0.25rem; }
.tf-sub { font-size: 0.75rem; color: #bbc9cf; }

.diff-panel {
  background: #0e0e0e;
  border: 1px solid rgba(60, 73, 78, 0.2);
  overflow: hidden;
}
.diff-header {
  background: #201f1f;
  padding: 0.75rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(60, 73, 78, 0.2);
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #bbc9cf;
}
.diff-rate { font-family: monospace; color: #859399; }
.diff-body { padding: 1.5rem; font-family: monospace; font-size: 0.6875rem; display: flex; flex-direction: column; gap: 0.5rem; overflow-x: auto; }
.diff-line { display: flex; gap: 1rem; white-space: nowrap; }
.diff-line .ln { width: 2rem; opacity: 0.3; }
.diff-line.neutral { color: #bbc9cf; }
.diff-line.removed { color: #ffb4ab; background: rgba(255, 180, 171, 0.1); padding: 2px 0; }
.diff-line.added { color: #7cecff; background: rgba(124, 236, 255, 0.1); padding: 2px 0; }

.diff-footer {
  padding: 1rem;
  border-top: 1px solid rgba(60, 73, 78, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.diff-author { font-size: 0.5625rem; font-weight: 700; text-transform: uppercase; color: #bbc9cf; letter-spacing: 0.05em; }

/* ── Roles ── */
.roles { background: #131313; }
.roles-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: -0.02em;
  text-align: center;
  margin-bottom: 4rem;
}
.roles-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}
@media (max-width: 900px) { .roles-grid { grid-template-columns: 1fr 1fr; } }
@media (max-width: 600px) { .roles-grid { grid-template-columns: 1fr; } }

.role-card {
  background: #2a2a2a;
  padding: 2rem;
  border-top: 2px solid var(--role-color);
}
.role-code {
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.3em;
  color: var(--role-color);
  margin-bottom: 1rem;
}
.role-card h3 {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.125rem;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 1rem;
}
.role-card ul { list-style: none; display: flex; flex-direction: column; gap: 0.75rem; }
.role-card li { font-size: 0.75rem; color: #bbc9cf; font-weight: 500; display: flex; align-items: flex-start; gap: 0.5rem; }
.role-slash { color: var(--role-color); }

/* ── CTA ── */
.cta-section {
  padding: 8rem 1.5rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.cta-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  background: rgba(164, 230, 255, 0.05);
  filter: blur(150px);
  pointer-events: none;
}
.cta-inner { position: relative; z-index: 1; max-width: 900px; margin: 0 auto; }
.cta-inner h2 {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(2rem, 5vw, 3.75rem);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: -0.05em;
  margin-bottom: 2rem;
  line-height: 1.1;
}
.cta-inner p { color: #bbc9cf; font-size: 1.125rem; margin-bottom: 3rem; max-width: 40rem; margin-left: auto; margin-right: auto; }
.cta-btns { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }

/* ── Footer ── */
.site-footer {
  background: #0e0e0e;
  border-top: 1px solid rgba(0, 209, 255, 0.05);
  padding: 3rem 1.5rem;
}
.footer-inner {
  max-width: 1440px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 2rem;
}
.brand-name {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.25rem;
  font-weight: 900;
  letter-spacing: -0.05em;
  color: #a4e6ff;
  margin-bottom: 0.5rem;
}
.footer-brand p {
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #353534;
}
.footer-links { display: flex; gap: 2rem; flex-wrap: wrap; }
.footer-links a {
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #353534;
  text-decoration: none;
  transition: color 0.2s;
}
.footer-links a:hover { color: #00d1ff; }
</style>
