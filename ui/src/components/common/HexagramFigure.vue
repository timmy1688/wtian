<template>
  <figure class="hexagram-figure">
    <figcaption class="hexagram-figure__caption">
      <span class="hexagram-figure__label">{{ label }}</span>
      <span class="hexagram-figure__name">{{ name }}</span>
    </figcaption>

    <div class="hexagram-figure__lines" role="img" :aria-label="ariaLabel">
      <div
        v-for="line in lines"
        :key="line.position"
        :class="['yao', { 'yao--moving': line.moving }]"
      >
        <span class="yao__pos">{{ line.positionLabel }}</span>
        <span :class="['yao__bar', line.isYang ? 'yao__bar--yang' : 'yao__bar--yin']">
          <i></i>
          <i v-if="!line.isYang"></i>
        </span>
        <span class="yao__mark" :title="line.moving ? (line.isYang ? '老阳' : '老阴') : ''">
          {{ line.moving ? (line.isYang ? '○' : '×') : '' }}
        </span>
      </div>
    </div>

    <div class="hexagram-figure__trigrams">
      <span>上 {{ formatTrigram(upper) }}</span>
      <span>下 {{ formatTrigram(lower) }}</span>
    </div>
  </figure>
</template>

<script setup>
import { computed } from 'vue';
import { YAO_POSITION_LABELS, formatTrigram } from '../../constants/yijing';

const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  name: {
    type: String,
    default: '',
  },
  // Bottom-to-top, 1 = yang, 0 = yin
  yao: {
    type: Array,
    default: () => [],
  },
  // 1-based positions to highlight
  moving: {
    type: Array,
    default: () => [],
  },
  upper: {
    type: String,
    default: '',
  },
  lower: {
    type: String,
    default: '',
  },
});

const lines = computed(() => props.yao
  .map((value, index) => ({
    position: index + 1,
    positionLabel: YAO_POSITION_LABELS[index],
    isYang: value === 1,
    moving: props.moving.includes(index + 1),
  }))
  .reverse());

const ariaLabel = computed(() => {
  const detail = lines.value
    .slice()
    .reverse()
    .map((line) => `${line.positionLabel}${line.isYang ? '阳' : '阴'}${line.moving ? '动' : ''}`)
    .join('，');
  return `${props.label}${props.name}：${detail}`;
});
</script>

<style scoped>
.hexagram-figure {
  flex: 1;
  min-width: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  padding: 28px 16px;
}

.hexagram-figure__caption {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.hexagram-figure__label {
  font-size: 12px;
  letter-spacing: 6px;
  color: var(--text-muted);
}

.hexagram-figure__name {
  padding-left: 0.2em;
  font-family: var(--font-serif);
  font-size: 30px;
  font-weight: 600;
  letter-spacing: 0.2em;
  color: var(--text);
}

.hexagram-figure__lines {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.yao {
  display: grid;
  grid-template-columns: 36px 132px 20px;
  align-items: center;
  gap: 12px;
}

.yao__pos {
  font-size: 12px;
  color: var(--text-muted);
  text-align: right;
}

.yao__bar {
  display: flex;
  gap: 20px;
  height: 9px;
}

.yao__bar i {
  flex: 1;
  background: var(--text);
}

.yao--moving .yao__bar i {
  background: var(--cinnabar);
}

.yao--moving .yao__pos {
  color: var(--cinnabar);
}

.yao__mark {
  font-size: 14px;
  color: var(--cinnabar);
}

.hexagram-figure__trigrams {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  justify-content: center;
  font-size: 12px;
  letter-spacing: 2px;
  color: var(--text-muted);
}

@media (max-width: 480px) {
  .yao {
    grid-template-columns: 30px 108px 16px;
    gap: 8px;
  }

  .yao__bar {
    gap: 16px;
    height: 8px;
  }

  .hexagram-figure__name {
    font-size: 26px;
  }
}
</style>
