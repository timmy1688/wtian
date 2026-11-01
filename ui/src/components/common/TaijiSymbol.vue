<template>
  <svg
    :class="['taiji-symbol', `taiji-symbol--${variant}`]"
    :width="size"
    :height="size"
    viewBox="-100 -100 200 200"
    role="img"
    :aria-label="bagua ? '太极八卦图' : '太极图'"
  >
    <g v-if="bagua" :class="['taiji-symbol__ring', { 'is-turning': spin }]">
      <circle class="taiji-symbol__stroke" r="97" />
      <circle class="taiji-symbol__ticks" r="90" />
      <circle class="taiji-symbol__stroke taiji-symbol__stroke--faint" r="60" />
      <g
        v-for="trigram in trigrams"
        :key="trigram.name"
        :transform="`rotate(${trigram.angle})`"
      >
        <template v-for="(line, lineIndex) in trigram.lines" :key="lineIndex">
          <rect
            v-for="(segment, segmentIndex) in line"
            :key="segmentIndex"
            class="taiji-symbol__yao"
            :x="segment.x"
            :y="-(TRIGRAM_INNER_RADIUS + lineIndex * TRIGRAM_LINE_GAP)"
            :width="segment.width"
            :height="TRIGRAM_LINE_HEIGHT"
          />
        </template>
      </g>
    </g>

    <g :class="['taiji-symbol__core', { 'is-turning': spin }]">
      <g :transform="`scale(${coreScale})`">
        <circle class="taiji-symbol__yin" r="48" />
        <path
          class="taiji-symbol__yang"
          d="M0,-48 A48,48 0 0,1 0,48 A24,24 0 0,1 0,0 A24,24 0 0,0 0,-48 Z"
        />
        <circle class="taiji-symbol__yin taiji-symbol__eye" cy="-24" r="6.5" />
        <circle class="taiji-symbol__yang taiji-symbol__eye" cy="24" r="6.5" />
        <circle class="taiji-symbol__stroke" r="48" />
      </g>
    </g>
  </svg>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  size: {
    type: [Number, String],
    default: 48,
  },
  bagua: {
    type: Boolean,
    default: false,
  },
  // Very slow rotation of the whole figure
  spin: {
    type: Boolean,
    default: false,
  },
  // "solid" for small marks, "line" for large faint backdrops
  variant: {
    type: String,
    default: 'solid',
    validator: (value) => ['solid', 'line'].includes(value),
  },
});

const TRIGRAM_INNER_RADIUS = 68;
const TRIGRAM_LINE_GAP = 7.5;
const TRIGRAM_LINE_HEIGHT = 3;
const TRIGRAM_WIDTH = 30;
const YIN_SEGMENT_RATIO = 0.42;

// 先天八卦, clockwise from the top (south up); lines are bottom (inner) to top (outer)
const XIANTIAN_ORDER = [
  { name: '乾', yao: [1, 1, 1] },
  { name: '巽', yao: [0, 1, 1] },
  { name: '坎', yao: [0, 1, 0] },
  { name: '艮', yao: [0, 0, 1] },
  { name: '坤', yao: [0, 0, 0] },
  { name: '震', yao: [1, 0, 0] },
  { name: '离', yao: [1, 0, 1] },
  { name: '兑', yao: [1, 1, 0] },
];

const buildLine = (isYang) => {
  const half = TRIGRAM_WIDTH / 2;
  if (isYang) {
    return [{ x: -half, width: TRIGRAM_WIDTH }];
  }
  const segment = TRIGRAM_WIDTH * YIN_SEGMENT_RATIO;
  return [
    { x: -half, width: segment },
    { x: half - segment, width: segment },
  ];
};

const trigrams = XIANTIAN_ORDER.map((trigram, index) => ({
  name: trigram.name,
  angle: index * 45,
  lines: trigram.yao.map((value) => buildLine(value === 1)),
}));

const coreScale = computed(() => (props.bagua ? 1.1 : 2));
</script>

<style scoped>
.taiji-symbol {
  display: inline-block;
  flex-shrink: 0;
  overflow: visible;
  color: var(--text);
}

.taiji-symbol__stroke {
  fill: none;
  stroke: currentColor;
  stroke-width: 1;
  vector-effect: non-scaling-stroke;
}

.taiji-symbol__stroke--faint {
  opacity: 0.4;
}

/* Fine compass graduations, as on a feng-shui luopan */
.taiji-symbol__ticks {
  fill: none;
  stroke: currentColor;
  stroke-width: 2.4;
  stroke-dasharray: 0.5 4.21;
  opacity: 0.5;
}

.taiji-symbol__yao {
  fill: currentColor;
  opacity: 0.8;
}

/* Solid: paper-white yang on ink-black yin */
.taiji-symbol--solid .taiji-symbol__yang {
  fill: currentColor;
}

.taiji-symbol--solid .taiji-symbol__yin {
  fill: var(--bg);
}

/* Line: outline only, so it can sit behind content at very low opacity */
.taiji-symbol--line .taiji-symbol__yang,
.taiji-symbol--line .taiji-symbol__yin {
  fill: none;
  stroke: currentColor;
  stroke-width: 1;
  vector-effect: non-scaling-stroke;
}

.taiji-symbol--line .taiji-symbol__yao {
  fill: none;
  stroke: currentColor;
  stroke-width: 1;
  vector-effect: non-scaling-stroke;
  opacity: 1;
}

.is-turning {
  transform-box: view-box;
  transform-origin: center;
  animation: slow-turn 240s linear infinite;
}
</style>
