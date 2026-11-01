<template>
  <section class="panel ai-loading" role="status" aria-live="polite">
    <div class="ai-loading__header">
      <TaijiSymbol class="ai-loading__taiji" :size="34" />
      <div class="ai-loading__text">
        <div class="ai-loading__title">{{ title }}</div>
        <div class="ai-loading__tip">
          <transition name="tip-fade" mode="out-in">
            <span :key="tipIndex">{{ tips[tipIndex] }}</span>
          </transition>
        </div>
      </div>
      <span class="ai-loading__elapsed">{{ elapsed }} 秒</span>
    </div>
    <div class="ai-loading__progress" aria-hidden="true">
      <span :style="{ width: `${progress}%` }"></span>
    </div>
    <div class="ai-loading__lines" aria-hidden="true">
      <span
        v-for="n in LINE_WIDTHS.length"
        :key="n"
        :style="{ width: `${LINE_WIDTHS[n - 1]}%`, animationDelay: `${(n - 1) * 0.25}s` }"
      ></span>
    </div>
  </section>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import TaijiSymbol from './TaijiSymbol.vue';

const props = defineProps({
  title: {
    type: String,
    default: '正在推演',
  },
  tips: {
    type: Array,
    default: () => ['正在整理信息', '正在推演分析', '正在撰写解读'],
  },
  // Typical response time; progress slows down asymptotically after this
  expectedSeconds: {
    type: Number,
    default: 20,
  },
});

const TIP_INTERVAL_SECONDS = 3;
const LINE_WIDTHS = [96, 88, 92, 70, 82];

const elapsed = ref(0);
let timer = null;

const tipIndex = computed(() => {
  if (props.tips.length === 0) {
    return 0;
  }
  return Math.floor(elapsed.value / TIP_INTERVAL_SECONDS) % props.tips.length;
});

// Never reaches 100% so the bar does not claim completion before the response arrives
const progress = computed(() => {
  const ratio = elapsed.value / props.expectedSeconds;
  return Math.min(95, Math.round((1 - Math.exp(-ratio * 1.6)) * 100));
});

onMounted(() => {
  timer = window.setInterval(() => {
    elapsed.value += 1;
  }, 1000);
});

onBeforeUnmount(() => {
  window.clearInterval(timer);
});
</script>

<style scoped>
.ai-loading__header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
}

.ai-loading__taiji {
  animation: slow-turn 8s linear infinite;
}

.ai-loading__text {
  flex: 1;
  min-width: 0;
}

.ai-loading__title {
  font-family: var(--font-serif);
  font-size: 19px;
  font-weight: 600;
  letter-spacing: 5px;
  color: var(--text);
}

.ai-loading__tip {
  margin-top: 6px;
  font-size: 13px;
  letter-spacing: 1px;
  color: var(--text-muted);
}

.ai-loading__elapsed {
  flex: 0 0 auto;
  align-self: flex-start;
  font-size: 12px;
  letter-spacing: 1px;
  color: var(--text-muted);
  font-variant-numeric: tabular-nums;
}

.ai-loading__progress {
  height: 1px;
  background: var(--line-soft);
  overflow: hidden;
}

.ai-loading__progress span {
  display: block;
  height: 100%;
  background: var(--text-soft);
  transition: width 0.8s var(--ease);
}

.ai-loading__lines {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 30px;
}

.ai-loading__lines span {
  height: 10px;
  background: rgba(236, 230, 218, 0.05);
  animation: breathe 2.4s ease-in-out infinite;
}

.tip-fade-enter-active,
.tip-fade-leave-active {
  transition: opacity 0.4s var(--ease);
}

.tip-fade-enter-from,
.tip-fade-leave-to {
  opacity: 0;
}
</style>
