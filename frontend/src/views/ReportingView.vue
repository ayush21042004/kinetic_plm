<template>
  <section class="reporting-view">
    <div class="hero-card">
      <div class="eyebrow">Reporting Workspace</div>
      <h1>Reporting is upcoming.</h1>
      <p>
        This page is reserved for dashboards, exports, KPI summaries, and operational analytics.
        The route and menu entry are ready, so we can add the real reporting modules next.
      </p>
    </div>

    <div class="content-grid">
      <article class="info-card">
        <h2>Planned Sections</h2>
        <ul>
          <li>ECO throughput and approval cycle reporting</li>
          <li>Product and BoM revision summaries</li>
          <li>Work center performance snapshots</li>
          <li>Export-ready operational views</li>
        </ul>
      </article>

      <article class="info-card muted">
        <h2>Status</h2>
        <p>Static placeholder active.</p>
        <p>Route available at <code>/reporting</code>.</p>
        <p>Menu available under <code>Master Data</code>.</p>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
</script>

<style lang="scss" scoped>
@use "../styles/variables" as v;

.reporting-view {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.hero-card,
.info-card {
  background: v.$white;
  border: 1px solid v.$border-color;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
}

.hero-card {
  padding: 2rem;

  h1 {
    margin: 0.4rem 0 0.75rem;
    font-size: 2rem;
    color: v.$text-primary;
  }

  p {
    margin: 0;
    max-width: 56rem;
    color: v.$text-secondary;
    line-height: 1.7;
  }
}

.eyebrow {
  display: inline-flex;
  padding: 0.35rem 0.7rem;
  border-radius: 999px;
  background: rgba(v.$primary-color, 0.08);
  color: v.$primary-color;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
}

.info-card {
  padding: 1.5rem;

  h2 {
    margin: 0 0 1rem;
    font-size: 1.1rem;
    color: v.$text-primary;
  }

  p {
    margin: 0 0 0.75rem;
    color: v.$text-secondary;
  }

  ul {
    margin: 0;
    padding-left: 1.1rem;
    color: v.$text-secondary;
    line-height: 1.8;
  }
}

.muted {
  background: linear-gradient(180deg, rgba(v.$primary-color, 0.03), rgba(148, 163, 184, 0.05));
}

code {
  padding: 0.15rem 0.4rem;
  border-radius: 0.4rem;
  background: rgba(15, 23, 42, 0.06);
  color: v.$text-primary;
}

@media (max-width: 900px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .hero-card {
    padding: 1.5rem;

    h1 {
      font-size: 1.6rem;
    }
  }
}

[data-theme="dark"] {
  .hero-card,
  .info-card {
    background: #111827;
    border-color: rgba(148, 163, 184, 0.18);
    box-shadow: none;
  }

  .hero-card h1,
  .info-card h2,
  code {
    color: #f8fafc;
  }

  .hero-card p,
  .info-card p,
  .info-card ul {
    color: #94a3b8;
  }

  .eyebrow {
    background: rgba(96, 165, 250, 0.14);
    color: #93c5fd;
  }

  .muted {
    background: linear-gradient(180deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95));
  }

  code {
    background: rgba(148, 163, 184, 0.12);
  }
}
</style>
