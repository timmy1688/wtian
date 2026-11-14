<template>
  <div class="page ops-page">
    <header class="ops-head">
      <h1 class="ops-head__title">记数</h1>
      <p class="ops-head__note">按上海时间分日。只记次数，不记生辰、问题、卦爻和解读。</p>
    </header>

    <p v-if="error" class="ops-state">{{ error }}</p>
    <p v-else-if="!report" class="ops-state">读取中</p>

    <template v-else>
      <section class="nums" aria-label="今天">
        <article v-for="item in report.headline" :key="item.key" class="num">
          <h2 class="num__label">{{ item.label }}</h2>
          <p class="num__value">{{ item.value }}</p>
          <p class="num__delta">{{ item.text }}</p>
          <p v-if="item.parts" class="num__parts">
            <span v-for="part in item.parts" :key="part.label">{{ part.label }} {{ part.value }}</span>
          </p>
        </article>
      </section>

      <section class="block">
        <h2 class="block__title">近三十日</h2>
        <svg class="chart" viewBox="0 0 640 220" role="img" aria-label="近三十日折线">
          <line class="chart__axis" x1="36" y1="16" x2="36" y2="176" />
          <line class="chart__axis" x1="36" y1="176" x2="624" y2="176" />
          <text class="chart__max" x="0" y="14">{{ lineMax }}</text>
          <polyline
            v-for="series in lineSeries"
            :key="series.key"
            fill="none"
            :stroke="series.color"
            stroke-width="1.6"
            :points="linePoints(series.key)"
          />
          <text
            v-for="tick in dayTicks"
            :key="tick.date"
            class="chart__tick"
            :x="tick.x"
            y="196"
            text-anchor="middle"
          >{{ tick.label }}</text>
        </svg>
        <ul class="legend">
          <li v-for="series in lineSeries" :key="series.key">
            <i :style="{ background: series.color }"></i>{{ series.label }}
          </li>
        </ul>
        <p class="block__note">{{ report.line_note }}</p>
      </section>

      <section class="block">
        <h2 class="block__title">详批与被挡住</h2>
        <svg class="chart" viewBox="0 0 640 220" role="img" aria-label="近三十日详批与被挡住">
          <line class="chart__axis" x1="36" y1="176" x2="624" y2="176" />
          <text class="chart__max" x="0" y="14">{{ barMax }}</text>
          <g v-for="(day, index) in report.days" :key="day.date">
            <rect
              v-for="(series, seriesIndex) in barSeries"
              :key="series.key"
              :x="barX(index, seriesIndex)"
              :y="barY(day[series.key])"
              :width="barWidth"
              :height="barH(day[series.key])"
              :fill="series.color"
            />
          </g>
        </svg>
        <ul class="legend">
          <li v-for="series in barSeries" :key="series.key">
            <i :style="{ background: series.color }"></i>{{ series.label }}
          </li>
        </ul>
        <p class="block__note">{{ report.bar_note }}</p>
      </section>

      <section class="block">
        <h2 class="block__title">近六个月</h2>
        <svg class="chart" viewBox="0 0 640 220" role="img" aria-label="近六个月">
          <line class="chart__axis" x1="36" y1="176" x2="624" y2="176" />
          <text class="chart__max" x="0" y="14">{{ monthMax }}</text>
          <g v-for="(month, index) in report.months" :key="month.month">
            <rect
              v-for="(series, seriesIndex) in lineSeries"
              :key="series.key"
              :x="monthX(index, seriesIndex)"
              :y="monthY(month[series.key])"
              :width="monthBarWidth"
              :height="monthH(month[series.key])"
              :fill="series.color"
            />
            <text class="chart__tick" :x="monthLabelX(index)" y="196" text-anchor="middle">{{ month.label }}</text>
          </g>
        </svg>
        <p class="block__note">{{ report.month_note }}</p>
      </section>

      <section class="block">
        <h2 class="block__title">三十日明细</h2>
        <div class="table-wrap">
          <table class="days">
            <thead>
              <tr>
                <th>日期</th>
                <th>打开</th>
                <th>首页</th>
                <th>排盘页</th>
                <th>起卦页</th>
                <th>排盘</th>
                <th>起卦</th>
                <th>详批</th>
                <th>八字</th>
                <th>六爻</th>
                <th>被挡住</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in report.table" :key="row.date" :class="{ 'is-today': row.date === report.today }">
                <td>{{ row.date }}</td>
                <td>{{ row.open }}</td>
                <td>{{ row.open_home }}</td>
                <td>{{ row.open_bazi }}</td>
                <td>{{ row.open_gua }}</td>
                <td>{{ row.paipan }}</td>
                <td>{{ row.qigua }}</td>
                <td>{{ row.xiangpi }}</td>
                <td>{{ row.xiangpi_bazi }}</td>
                <td>{{ row.xiangpi_gua }}</td>
                <td>{{ row.blocked }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import http from '../api/request';

const report = ref(null);
const error = ref('');

const lineSeries = [
  { key: 'open', label: '打开', color: '#7c766c' },
  { key: 'paipan', label: '排盘', color: '#b8b1a4' },
  { key: 'qigua', label: '起卦', color: '#c3a46e' },
  { key: 'xiangpi', label: '详批', color: '#ece6da' },
];
const barSeries = [
  { key: 'xiangpi', label: '详批', color: '#c3a46e' },
  { key: 'blocked', label: '被挡住', color: '#b4442f' },
];

const plot = { left: 36, right: 624, top: 16, bottom: 176 };

const maxOf = (rows, keys) => Math.max(1, ...rows.flatMap((row) => keys.map((key) => row[key] || 0)));

const lineMax = computed(() => (report.value ? maxOf(report.value.days, lineSeries.map((s) => s.key)) : 1));
const barMax = computed(() => (report.value ? maxOf(report.value.days, barSeries.map((s) => s.key)) : 1));
const monthMax = computed(() => (report.value ? maxOf(report.value.months, lineSeries.map((s) => s.key)) : 1));

const yOf = (value, max) => plot.bottom - ((plot.bottom - plot.top) * value) / max;

const linePoints = (key) => {
  const days = report.value.days;
  const step = days.length > 1 ? (plot.right - plot.left) / (days.length - 1) : 0;
  return days.map((day, index) => `${plot.left + step * index},${yOf(day[key], lineMax.value)}`).join(' ');
};

const dayTicks = computed(() => {
  if (!report.value) {
    return [];
  }
  const days = report.value.days;
  const step = days.length > 1 ? (plot.right - plot.left) / (days.length - 1) : 0;
  return days
    .map((day, index) => ({ date: day.date, label: day.date.slice(5), x: plot.left + step * index, index }))
    .filter((tick) => tick.index % 5 === 0 || tick.index === days.length - 1);
});

const groupWidth = computed(() => (plot.right - plot.left) / 30);
const barWidth = computed(() => Math.max(2, groupWidth.value * 0.32));

const barX = (index, seriesIndex) => plot.left + groupWidth.value * index + seriesIndex * (barWidth.value + 1);
const barY = (value) => yOf(value, barMax.value);
const barH = (value) => plot.bottom - barY(value);

const monthGroup = (plot.right - plot.left) / 6;
const monthBarWidth = 14;
const monthX = (index, seriesIndex) => (
  plot.left + monthGroup * index + (monthGroup - lineSeries.length * (monthBarWidth + 3)) / 2
  + seriesIndex * (monthBarWidth + 3)
);
const monthLabelX = (index) => plot.left + monthGroup * index + monthGroup / 2;
const monthY = (value) => yOf(value, monthMax.value);
const monthH = (value) => plot.bottom - monthY(value);

onMounted(async () => {
  try {
    const { data } = await http.get('/ops/stats');
    report.value = data;
  } catch (err) {
    error.value = '记数没有读到';
  }
});
</script>

<style scoped>
.ops-head {
  margin-bottom: 28px;
}

.ops-head__title {
  margin: 0;
  font-family: var(--font-serif);
  font-size: 36px;
  font-weight: 600;
  letter-spacing: 10px;
}

.ops-head__note,
.ops-state,
.block__note {
  margin: 10px 0 0;
  font-size: 13px;
  line-height: 1.8;
  color: var(--text-muted);
}

.nums {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  border-top: 1px solid var(--line-soft);
  border-bottom: 1px solid var(--line-soft);
}

.num {
  padding: 18px 12px 16px;
}

.num + .num {
  border-left: 1px solid var(--line-soft);
}

.num__label {
  margin: 0;
  font-family: var(--font-serif);
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 4px;
  color: var(--text-soft);
}

.num__value {
  margin: 8px 0 0;
  font-family: var(--font-serif);
  font-size: 32px;
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
}

.num__delta,
.num__parts {
  margin: 6px 0 0;
  font-size: 12px;
  color: var(--text-muted);
}

.num__parts {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.block {
  margin-top: 40px;
}

.block__title {
  margin: 0 0 12px;
  font-family: var(--font-serif);
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 4px;
}

.chart {
  width: 100%;
  height: auto;
}

.chart__axis {
  stroke: rgba(236, 230, 218, 0.16);
  stroke-width: 1;
}

.chart__max,
.chart__tick {
  fill: #7c766c;
  font-size: 11px;
}

.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 18px;
  margin: 8px 0 0;
  padding: 0;
  list-style: none;
  font-size: 12px;
  color: var(--text-muted);
}

.legend i {
  display: inline-block;
  width: 14px;
  height: 2px;
  margin-right: 6px;
  vertical-align: middle;
}

.table-wrap {
  overflow-x: auto;
  border-top: 1px solid var(--line-soft);
}

.days {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  font-variant-numeric: tabular-nums;
}

.days th,
.days td {
  padding: 8px 10px;
  text-align: right;
  white-space: nowrap;
  border-bottom: 1px solid var(--line-soft);
}

.days th:first-child,
.days td:first-child {
  text-align: left;
}

.days th {
  font-weight: 500;
  color: var(--text-muted);
}

.days .is-today td {
  color: var(--accent);
}

@media (max-width: 768px) {
  .ops-head__title {
    font-size: 28px;
  }

  .nums {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .num:nth-child(2n + 1) {
    border-left: none;
  }

  .num:nth-child(n + 3) {
    border-top: 1px solid var(--line-soft);
  }
}
</style>
