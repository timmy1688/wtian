<template>
  <div class="page bazi-page">
    <PageHero title="八字" seal="命理" subtitle="知命者不怨天" />

    <!-- 输入表单 -->
    <section class="panel">
      <a-form
        ref="formRef"
        :model="formState"
        :rules="rules"
        layout="vertical"
        :required-mark="false"
        @finish="fetchBazi"
        @finish-failed="onFinishFailed"
      >
        <div class="form-row form-row--compact">
          <a-form-item label="日历类型" name="isLunar">
            <a-radio-group v-model:value="formState.isLunar" button-style="solid" size="large">
              <a-radio-button :value="false">公历</a-radio-button>
              <a-radio-button :value="true">农历</a-radio-button>
            </a-radio-group>
          </a-form-item>

          <a-form-item label="性别" name="gender">
            <a-radio-group v-model:value="formState.gender" button-style="solid" size="large">
              <a-radio-button value="boy">男</a-radio-button>
              <a-radio-button value="girl">女</a-radio-button>
            </a-radio-group>
          </a-form-item>
        </div>

        <div class="form-row">
          <a-form-item
            :label="formState.isLunar ? '出生日期（农历）' : '出生日期（公历）'"
            name="birthDate"
            :extra="formState.isLunar ? '请按农历月、日选择，如农历正月十五请选 1 月 15 日' : ''"
          >
            <a-date-picker
              v-model:value="formState.birthDate"
              size="large"
              format="YYYY-MM-DD"
              placeholder="请选择出生日期"
              :disabled-date="disableFutureDate"
              :default-picker-value="defaultPickerValue"
              :input-read-only="touchDevice"
              style="width: 100%"
            />
          </a-form-item>

          <a-form-item label="出生时辰" name="hour" extra="不确定时辰可选最接近的时段">
            <a-select
              v-model:value="formState.hour"
              size="large"
              placeholder="请选择出生时辰"
              :options="SHICHEN_OPTIONS"
              :list-height="320"
            />
          </a-form-item>
        </div>

        <a-form-item label="关注方向" name="demand">
          <div class="chip-group" role="radiogroup" aria-label="关注方向">
            <button
              v-for="item in BAZI_DEMAND_OPTIONS"
              :key="item"
              type="button"
              role="radio"
              :aria-checked="formState.demand === item"
              :class="['chip', { 'chip--active': formState.demand === item }]"
              @click="formState.demand = item"
            >
              {{ item }}
            </button>
          </div>
        </a-form-item>

        <a-button
          type="primary"
          html-type="submit"
          :loading="loadingBazi"
          size="large"
          block
          class="btn-main"
        >
          {{ loadingBazi ? '排盘中...' : (baziResult ? '重新排盘' : '开始排盘') }}
        </a-button>
      </a-form>
    </section>

    <!-- 排盘结果 -->
    <transition name="fade-slide">
      <section v-if="baziResult" ref="resultRef" class="panel">
        <div class="section-heading">
          <h2 class="section-heading__title">排盘结果</h2>
          <span class="section-heading__hint">{{ genderLabel }} · {{ submittedDemand }}</span>
        </div>

        <div class="birth-info">
          <div class="birth-info__item">
            <span class="birth-info__label">公历</span>
            <span class="birth-info__value">{{ baziResult.new_birth }}</span>
          </div>
          <div class="birth-info__item">
            <span class="birth-info__label">农历</span>
            <span class="birth-info__value">{{ baziResult.old_birth }}</span>
          </div>
        </div>

        <div class="pillars" role="table" aria-label="四柱八字">
          <div class="pillars__row pillars__row--head" role="row">
            <span class="pillars__cell pillars__cell--label" role="rowheader"></span>
            <span
              v-for="pillar in pillars"
              :key="pillar.name"
              :class="['pillars__cell', 'pillars__name', { 'is-day': pillar.isDay }]"
              role="columnheader"
            >
              {{ pillar.name }}
            </span>
          </div>
          <div class="pillars__row" role="row">
            <span class="pillars__cell pillars__cell--label" role="rowheader">十神</span>
            <span
              v-for="pillar in pillars"
              :key="pillar.name"
              :class="['pillars__cell', 'pillars__god', { 'is-day': pillar.isDay }]"
              role="cell"
            >
              {{ pillar.god }}
            </span>
          </div>
          <div class="pillars__row" role="row">
            <span class="pillars__cell pillars__cell--label" role="rowheader">天干</span>
            <span
              v-for="pillar in pillars"
              :key="pillar.name"
              class="pillars__cell"
              role="cell"
            >
              <span class="bazi-char" :style="{ '--wx-color': pillar.gan.color }">
                {{ pillar.gan.char }}
                <small>{{ pillar.gan.wuxing }}</small>
              </span>
            </span>
          </div>
          <div class="pillars__row" role="row">
            <span class="pillars__cell pillars__cell--label" role="rowheader">地支</span>
            <span
              v-for="pillar in pillars"
              :key="pillar.name"
              class="pillars__cell"
              role="cell"
            >
              <span class="bazi-char" :style="{ '--wx-color': pillar.zhi.color }">
                {{ pillar.zhi.char }}
                <small>{{ pillar.zhi.wuxing }}</small>
              </span>
            </span>
          </div>
        </div>

        <div class="summary-tags">
          <span v-if="dayMaster" class="summary-tag">
            日主：{{ dayMaster.char }}{{ dayMaster.wuxing }}
          </span>
          <span v-if="strengthText" class="summary-tag">{{ strengthText }}</span>
          <span v-if="favorableText" class="summary-tag">{{ favorableText }}</span>
          <span v-if="strongestWuxing" class="summary-tag">最旺：{{ strongestWuxing }}</span>
          <span :class="['summary-tag', { 'summary-tag--warn': missingWuxing.length > 0 }]">
            {{ missingWuxing.length > 0 ? `五行缺${missingWuxing.join('、')}` : '五行俱全' }}
          </span>
        </div>

        <div class="wuxing-list">
          <div v-for="item in wuxingList" :key="item.name" class="wuxing-item">
            <span class="wuxing-item__name" :style="{ color: item.color }">{{ item.name }}</span>
            <div class="wuxing-item__bar">
              <div
                class="wuxing-item__fill"
                :style="{ width: `${item.percent}%`, background: item.color, color: item.color }"
              ></div>
            </div>
            <span class="wuxing-item__value">{{ item.count }}个 · {{ item.percent }}%</span>
          </div>
        </div>

        <div v-if="dayunSteps.length > 0" class="dayun">
          <div class="dayun__head">
            <span class="dayun__title">大运</span>
            <span class="dayun__hint">{{ dayunHint }}</span>
          </div>
          <ol class="dayun__list">
            <li
              v-for="step in dayunSteps"
              :key="step.ganzhi"
              :class="['dayun__item', { 'dayun__item--current': step.ganzhi === currentDayun }]"
              :aria-current="step.ganzhi === currentDayun ? 'step' : undefined"
            >
              <span class="dayun__ganzhi">{{ step.ganzhi }}</span>
              <span class="dayun__god">{{ step.gan_shishen }}</span>
              <span class="dayun__years">{{ step.start_year }}</span>
              <span class="dayun__age">{{ step.start_age }}岁</span>
            </li>
          </ol>
        </div>

        <div v-if="ai.phase.value === 'idle'" class="analyze-action">
          <a-button
            type="primary"
            size="large"
            class="btn-main"
            @click="fetchFenxi"
          >
            详批命盘
          </a-button>
          <p class="action-tip">解读每日有次数限制，请确认以上信息无误</p>
        </div>
      </section>
    </transition>

    <!-- AI 分析 -->
    <div ref="analysisRef" class="analysis-anchor">
      <transition name="fade-slide" mode="out-in">
        <AiLoadingCard
          v-if="ai.phase.value === 'waiting'"
          title="正在参详命盘"
          :tips="loadingTips"
          :expected-seconds="6"
        />
        <AnalysisResult
          v-else-if="ai.content.value"
          title="命盘分析"
          :content="ai.content.value"
          :copy-prefix="copyPrefix"
          :streaming="ai.phase.value === 'streaming'"
        />
      </transition>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, reactive, ref } from 'vue';
import { message } from 'ant-design-vue';
import dayjs from 'dayjs';
import 'dayjs/locale/zh-cn';
import http, { getErrorMessage, getServerMessage } from '../api/request';
import { useAiStream } from '../composables/useAiStream';
import AiLoadingCard from './common/AiLoadingCard.vue';
import AnalysisResult from './common/AnalysisResult.vue';
import PageHero from './common/PageHero.vue';
import {
  BAZI_CHAR_COUNT,
  BAZI_DEMAND_OPTIONS,
  GAN_WUXING,
  PILLAR_NAMES,
  SHICHEN_OPTIONS,
  WUXING_COLORS,
  WUXING_ORDER,
  ZHI_WUXING,
} from '../constants/bazi';
import { isTouchDevice, scrollToElement } from '../utils/dom';

dayjs.locale('zh-cn');

const DAY_PILLAR_INDEX = 2;
const DEFAULT_PICKER_YEAR = 1990;

const loadingTips = [
  '正在梳理四柱干支',
  '正在推演五行生克',
  '正在分析十神格局',
  '正在结合关注方向撰写解读',
];

const formRef = ref(null);
const resultRef = ref(null);
const analysisRef = ref(null);

const formState = reactive({
  isLunar: false,
  gender: undefined,
  birthDate: null,
  hour: undefined,
  demand: BAZI_DEMAND_OPTIONS[0],
});

const rules = {
  gender: [{ required: true, message: '请选择性别' }],
  birthDate: [{ required: true, type: 'object', message: '请选择出生日期' }],
  hour: [{ required: true, type: 'number', message: '请选择出生时辰' }],
};

const baziResult = ref(null);
const submittedDemand = ref('');
const submittedBirth = ref(null);
const loadingBazi = ref(false);
const ai = useAiStream();

const touchDevice = isTouchDevice();
const defaultPickerValue = dayjs(`${DEFAULT_PICKER_YEAR}-01-01`);

const disableFutureDate = (current) => Boolean(current) && current.isAfter(dayjs(), 'day');

const genderLabel = computed(() => (baziResult.value?.gender === 'girl' ? '女命' : '男命'));

const buildChar = (char, map) => {
  const wuxing = map[char] || '';
  return { char, wuxing, color: WUXING_COLORS[wuxing] || 'var(--text)' };
};

const pillars = computed(() => {
  if (!baziResult.value) {
    return [];
  }
  const { bazi = [], shishen = [] } = baziResult.value;
  return bazi.map((ganzhi, index) => ({
    name: PILLAR_NAMES[index],
    isDay: index === DAY_PILLAR_INDEX,
    // The day stem is the reference point itself, conventionally shown as 日元
    god: index === DAY_PILLAR_INDEX ? '日元' : shishen[index],
    gan: buildChar(ganzhi[0], GAN_WUXING),
    zhi: buildChar(ganzhi[1], ZHI_WUXING),
  }));
});

const dayMaster = computed(() => pillars.value[DAY_PILLAR_INDEX]?.gan || null);

const chart = computed(() => baziResult.value?.chart || null);

const strengthText = computed(() => (chart.value?.strength?.level ? `日主${chart.value.strength.level}` : ''));

const favorableText = computed(() => {
  const favorable = chart.value?.favorable?.favorable || [];
  return favorable.length > 0 ? `喜用：${favorable.join('、')}` : '';
});

const dayunSteps = computed(() => chart.value?.dayun?.steps || []);

const currentDayun = computed(() => chart.value?.current_dayun?.ganzhi || '');

const dayunHint = computed(() => {
  const dayun = chart.value?.dayun;
  return dayun ? `${dayun.direction} · ${dayun.start_desc}` : '';
});

const wuxingList = computed(() => {
  const wuxing = baziResult.value?.wuxing || {};
  return WUXING_ORDER.map((name) => {
    const raw = Number(wuxing[name]) || 0;
    return {
      name,
      color: WUXING_COLORS[name],
      percent: Number(raw.toFixed(1)),
      count: Math.round((raw * BAZI_CHAR_COUNT) / 100),
    };
  });
});

const missingWuxing = computed(() => wuxingList.value
  .filter((item) => item.count === 0)
  .map((item) => item.name));

const strongestWuxing = computed(() => {
  const max = Math.max(...wuxingList.value.map((item) => item.count));
  if (max <= 0) {
    return '';
  }
  return wuxingList.value
    .filter((item) => item.count === max)
    .map((item) => item.name)
    .join('、');
});

const copyPrefix = computed(() => {
  if (!baziResult.value) {
    return '';
  }
  return [
    `【八字命盘】${genderLabel.value}`,
    `公历：${baziResult.value.new_birth}`,
    `农历：${baziResult.value.old_birth}`,
    `八字：${baziResult.value.bazi.join(' ')}`,
  ].join('\n');
});

const onFinishFailed = () => {
  message.warning('请先补全出生信息');
};

const fetchBazi = async () => {
  const birth = `${formState.birthDate.format('YYYYMMDD')} ${String(formState.hour).padStart(2, '0')}`;
  loadingBazi.value = true;
  try {
    const { data } = await http.post('/bazi/paipan', {
      birth,
      gender: formState.gender,
      is_lunar: formState.isLunar,
    });
    if (!data || typeof data !== 'object' || !Array.isArray(data.bazi)) {
      message.error(getServerMessage(data) || '服务器返回数据格式错误');
      return;
    }
    baziResult.value = data;
    ai.reset();
    submittedDemand.value = formState.demand;
    submittedBirth.value = { birth, is_lunar: formState.isLunar };
    await nextTick();
    scrollToElement(resultRef.value);
  } catch (error) {
    console.error('fetchBazi failed:', error);
    message.error(getErrorMessage(error, '排盘失败，请检查输入后重试'));
  } finally {
    loadingBazi.value = false;
  }
};

const fetchFenxi = async () => {
  if (!baziResult.value || ai.busy.value) {
    return;
  }
  const request = ai.start('/bazi/fenxi/stream', {
    gender: baziResult.value.gender,
    ...submittedBirth.value,
    bazi: baziResult.value.bazi,
    demand: submittedDemand.value || BAZI_DEMAND_OPTIONS[0],
  });
  await nextTick();
  scrollToElement(analysisRef.value);
  const outcome = await request;
  if (outcome.ok || outcome.aborted) {
    return;
  }
  if (outcome.data?.status === 'limited') {
    message.warning(outcome.message);
  } else {
    message.error(outcome.message);
  }
};
</script>

<style scoped>
/* ========== Birth info ========== */
.birth-info {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px 48px;
  margin-bottom: 36px;
}

.birth-info__item {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.birth-info__label {
  font-size: 12px;
  letter-spacing: 3px;
  color: var(--text-muted);
}

.birth-info__value {
  font-family: var(--font-serif);
  font-size: 17px;
  letter-spacing: 1px;
  color: var(--text);
}

/* ========== Four pillars ========== */
.pillars {
  padding: 8px 0 12px;
  margin-bottom: 32px;
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
}

.pillars__row {
  display: grid;
  grid-template-columns: 56px repeat(4, minmax(0, 1fr));
  align-items: center;
  padding: 8px 0;
}

.pillars__row--head {
  border-bottom: 1px solid var(--line-soft);
  margin-bottom: 8px;
}

.pillars__cell {
  display: flex;
  justify-content: center;
  text-align: center;
}

.pillars__cell--label {
  font-size: 12px;
  letter-spacing: 2px;
  color: var(--text-muted);
}

.pillars__name {
  font-family: var(--font-serif);
  font-size: 15px;
  letter-spacing: 4px;
  color: var(--text-muted);
}

.pillars__god {
  font-family: var(--font-serif);
  font-size: 15px;
  letter-spacing: 1px;
  color: var(--text-soft);
}

.is-day {
  color: var(--accent);
}

.bazi-char {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  font-family: var(--font-serif);
  font-size: 40px;
  font-weight: 600;
  color: var(--wx-color);
}

.bazi-char small {
  position: absolute;
  right: 2px;
  bottom: 4px;
  font-family: var(--font-sans);
  font-size: 10px;
  font-weight: 400;
  color: var(--text-muted);
}

/* ========== Summary ========== */
.summary-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px 36px;
  margin-bottom: 36px;
}

.summary-tag {
  font-family: var(--font-serif);
  font-size: 15px;
  letter-spacing: 2px;
  color: var(--text-soft);
}

.summary-tag--warn {
  color: var(--cinnabar);
}

/* ========== Wuxing ========== */
.wuxing-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
  max-width: 560px;
  margin: 0 auto 40px;
}

.wuxing-item {
  display: grid;
  grid-template-columns: 24px minmax(0, 1fr) 92px;
  align-items: center;
  gap: 16px;
}

.wuxing-item__name {
  font-family: var(--font-serif);
  font-size: 17px;
  font-weight: 600;
}

.wuxing-item__bar {
  height: 2px;
  background: var(--line-soft);
}

.wuxing-item__fill {
  height: 100%;
  transition: width 1.2s var(--ease);
}

.wuxing-item__value {
  font-size: 12px;
  color: var(--text-muted);
  text-align: right;
  font-variant-numeric: tabular-nums;
}

/* ========== Da yun (10-year luck pillars) ========== */
.dayun {
  margin-bottom: 40px;
}

.dayun__head {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 4px 16px;
  margin-bottom: 14px;
}

.dayun__title {
  font-family: var(--font-serif);
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 6px;
  color: var(--text);
}

.dayun__hint {
  font-size: 12px;
  color: var(--text-muted);
}

.dayun__list {
  display: grid;
  grid-template-columns: repeat(8, minmax(64px, 1fr));
  margin: 0;
  padding: 0;
  list-style: none;
  overflow-x: auto;
  scrollbar-width: thin;
  border-top: 1px solid var(--line-soft);
}

.dayun__item {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  padding: 14px 4px 10px;
}

.dayun__item + .dayun__item {
  border-left: 1px solid var(--line-soft);
}

.dayun__item--current::before {
  content: '';
  position: absolute;
  top: -1px;
  left: 20%;
  right: 20%;
  height: 1px;
  background: var(--accent);
}

.dayun__ganzhi {
  font-family: var(--font-serif);
  font-size: 19px;
  font-weight: 600;
  letter-spacing: 2px;
  color: var(--text-soft);
}

.dayun__item--current .dayun__ganzhi {
  color: var(--accent);
}

.dayun__god {
  font-size: 12px;
  color: var(--text-muted);
}

.dayun__years,
.dayun__age {
  font-size: 11px;
  color: var(--text-muted);
  font-variant-numeric: tabular-nums;
}

@media (max-width: 640px) {
  .dayun__list {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }

  .dayun__item:nth-child(4n + 1) {
    border-left: none;
  }

  .dayun__item:nth-child(n + 5) {
    border-top: 1px solid var(--line-soft);
  }

  .dayun__ganzhi {
    font-size: 17px;
  }
}

.analyze-action {
  text-align: center;
}

.analysis-anchor {
  scroll-margin-top: calc(var(--header-height) + 16px);
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .birth-info {
    flex-direction: column;
    align-items: center;
    gap: 6px;
    margin-bottom: 24px;
  }

  .birth-info__value {
    font-size: 15px;
  }

  .pillars__row {
    grid-template-columns: 34px repeat(4, minmax(0, 1fr));
  }

  .pillars__name {
    font-size: 14px;
    letter-spacing: 2px;
  }

  .pillars__god {
    font-size: 14px;
  }

  .bazi-char {
    width: 54px;
    height: 54px;
    font-size: 34px;
  }

  .summary-tags {
    gap: 8px 22px;
  }

  .summary-tag {
    font-size: 14px;
  }

  .analyze-action .ant-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .pillars__row {
    grid-template-columns: 28px repeat(4, minmax(0, 1fr));
  }

  .pillars__cell--label {
    font-size: 11px;
    letter-spacing: 0;
  }

  .bazi-char {
    width: 46px;
    height: 46px;
    font-size: 30px;
  }

  .bazi-char small {
    font-size: 9px;
    right: 0;
  }

  .wuxing-item {
    grid-template-columns: 20px minmax(0, 1fr) 76px;
    gap: 10px;
  }
}
</style>
