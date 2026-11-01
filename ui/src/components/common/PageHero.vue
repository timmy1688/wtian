<template>
  <header class="page-hero">
    <div class="page-hero__title-row">
      <h1 class="page-hero__title">{{ title }}</h1>
      <span v-if="seal" class="seal page-hero__seal" aria-hidden="true">{{ seal }}</span>
    </div>
    <p v-if="subtitle" class="page-hero__subtitle">{{ subtitle }}</p>
    <div class="divider" aria-hidden="true"></div>
  </header>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: '',
  },
  // Two characters read best inside the vertical seal
  seal: {
    type: String,
    default: '',
  },
});
</script>

<style scoped>
.page-hero {
  text-align: center;
  padding: 16px 16px 8px;
  margin-bottom: 48px;
}

.page-hero__title-row {
  display: inline-flex;
  align-items: flex-end;
  gap: 6px;
}

.page-hero__title {
  margin: 0;
  padding-left: 0.4em;
  font-family: var(--font-serif);
  font-size: 44px;
  font-weight: 600;
  line-height: 1.2;
  letter-spacing: 0.4em;
  color: var(--text);
}

.page-hero__seal {
  width: 30px;
  height: 30px;
  margin-bottom: 6px;
  font-size: 12px;
}

.page-hero__subtitle {
  margin-top: 18px;
  font-family: var(--font-serif);
  font-size: 14px;
  letter-spacing: 6px;
  color: var(--text-muted);
}

@media (max-width: 768px) {
  .page-hero {
    padding: 8px 8px 0;
    margin-bottom: 28px;
  }

  .page-hero__title {
    font-size: 32px;
  }

  .page-hero__seal {
    width: 26px;
    height: 26px;
    font-size: 11px;
    margin-bottom: 4px;
  }

  .page-hero__subtitle {
    margin-top: 12px;
    font-size: 13px;
    letter-spacing: 3px;
  }
}
</style>
