<template>
  <div class="page gua-page">
    <PageHero title="六爻" seal="卜筮" subtitle="无事不占　不动不占" />

    <ol class="steps" aria-label="占卜步骤">
      <li
        v-for="(step, index) in stepItems"
        :key="step.title"
        :class="['steps__item', { 'is-done': index < currentStep, 'is-current': index === currentStep }]"
        :aria-current="index === currentStep ? 'step' : undefined"
      >
        <span class="steps__numeral">{{ step.numeral }}</span>
        <span class="steps__title">{{ step.title }}</span>
      </li>
    </ol>

    <transition name="fade-slide" mode="out-in" @after-enter="onStepEntered">
      <!-- 第一步：填写问题 -->
      <section v-if="!hexagramData" key="form" class="panel">
        <div class="section-heading">
          <h2 class="section-heading__title">心中所问</h2>
        </div>

        <a-form
          ref="formRef"
          :model="formState"
          :rules="rules"
          layout="vertical"
          :required-mark="false"
          @finish="castHexagram"
          @finish-failed="onFinishFailed"
        >
          <a-form-item label="性别" name="gender">
            <a-radio-group v-model:value="formState.gender" button-style="solid" size="large">
              <a-radio-button value="boy">男</a-radio-button>
              <a-radio-button value="girl">女</a-radio-button>
            </a-radio-group>
          </a-form-item>

          <a-form-item label="占卜事项" name="category">
            <div class="chip-group" role="radiogroup" aria-label="占卜事项">
              <button
                v-for="item in GUA_DEMAND_OPTIONS"
                :key="item"
                type="button"
                role="radio"
                :aria-checked="formState.category === item"
                :class="['chip', { 'chip--active': formState.category === item }]"
                @click="selectCategory(item)"
              >
                {{ item }}
              </button>
            </div>
          </a-form-item>

          <a-form-item
            label="具体问题（选填）"
            name="question"
            extra="描述越具体，解读越贴合。一事一占，同一问题不宜反复起卦。"
          >
            <a-textarea
              v-model:value="formState.question"
              :placeholder="questionPlaceholder"
              :maxlength="QUESTION_MAX_LENGTH"
              :auto-size="{ minRows: 2, maxRows: 4 }"
              show-count
            />
          </a-form-item>

          <a-alert
            type="info"
            show-icon
            class="cast-tip"
            message="起卦方式"
            description="采用传统「三枚铜钱摇卦法」：每次抛掷三枚铜钱定一爻，自下而上六次成卦，老阴老阳为动爻。起卦前请静心默念所问之事。"
          />

          <a-button
            type="primary"
            html-type="submit"
            :loading="casting"
            size="large"
            block
            class="btn-main"
          >
            {{ casting ? '摇卦中...' : '诚心起卦' }}
          </a-button>
        </a-form>
      </section>

      <!-- 第二步：卦象 -->
      <section v-else key="hexagram" ref="hexagramRef" class="panel">
        <div class="section-heading">
          <h2 class="section-heading__title">卦象结果</h2>
          <span class="section-heading__hint">{{ genderLabel }} · {{ demandText }}</span>
        </div>

        <div class="hexagram-pair">
          <HexagramFigure
            label="本卦"
            :name="hexagramData.bengua.gua"
            :yao="hexagramData.bengua.yao"
            :moving="dongyao"
            :upper="hexagramData.bengua.shanggua"
            :lower="hexagramData.bengua.xiagua"
          />
          <div class="hexagram-pair__arrow" aria-hidden="true">
            <span>{{ dongyao.length > 0 ? '变' : '静' }}</span>
          </div>
          <HexagramFigure
            label="变卦"
            :name="hexagramData.biangua.gua"
            :yao="hexagramData.biangua.yao"
            :upper="hexagramData.biangua.shanggua"
            :lower="hexagramData.biangua.xiagua"
          />
        </div>

        <div class="dongyao-info">
          <span class="dongyao-info__label">动爻</span>
          <span class="dongyao-info__value">{{ dongyaoText }}</span>
          <span v-if="dongyao.length === 0" class="dongyao-info__note">六爻安静，以本卦卦辞为主</span>
          <span v-else class="dongyao-info__note">○ 老阳　× 老阴</span>
        </div>

        <div class="action-row">
          <a-button
            v-if="ai.phase.value === 'idle'"
            type="primary"
            size="large"
            class="btn-main"
            @click="analyzeHexagram"
          >
            解卦
          </a-button>
          <a-button size="large" class="btn-ghost" :disabled="ai.busy.value" @click="resetHexagram">
            <template #icon><RedoOutlined /></template>
            重新起卦
          </a-button>
        </div>
        <p v-if="ai.phase.value === 'idle'" class="action-tip">解卦每日有次数限制</p>
      </section>
    </transition>

    <!-- 第三步：解读 -->
    <div ref="analysisRef" class="analysis-anchor">
      <transition name="fade-slide" mode="out-in">
        <AiLoadingCard
          v-if="ai.phase.value === 'waiting'"
          title="正在参详卦象"
          :tips="loadingTips"
          :expected-seconds="6"
        />
        <AnalysisResult
          v-else-if="ai.content.value"
          title="卦象解读"
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
import { RedoOutlined } from '@ant-design/icons-vue';
import http, { getErrorMessage } from '../api/request';
import { useAiStream } from '../composables/useAiStream';
import AiLoadingCard from './common/AiLoadingCard.vue';
import AnalysisResult from './common/AnalysisResult.vue';
import HexagramFigure from './common/HexagramFigure.vue';
import PageHero from './common/PageHero.vue';
import { GUA_DEMAND_OPTIONS, formatDongyao } from '../constants/yijing';
import { scrollToElement } from '../utils/dom';

const QUESTION_MAX_LENGTH = 60;

const QUESTION_PLACEHOLDERS = {
  事业: '例如：下半年适合换工作吗？',
  爱情: '例如：和现在的对象能否长久？',
  财运: '例如：近期的投资计划是否可行？',
  健康: '例如：近期身体状况需要注意什么？',
  学业: '例如：这次考试能否顺利通过？',
  其他: '请简要描述你想问的事情',
};

const loadingTips = [
  '正在参详本卦卦意',
  '正在推敲动爻爻辞',
  '正在比对变卦趋势',
  '正在结合所问之事撰写解读',
];

const stepItems = [
  { numeral: '壹', title: '心中所问' },
  { numeral: '贰', title: '摇卦成象' },
  { numeral: '叁', title: '解卦' },
];

const formRef = ref(null);
const hexagramRef = ref(null);
const analysisRef = ref(null);

const formState = reactive({
  gender: undefined,
  category: undefined,
  question: '',
});

const rules = {
  gender: [{ required: true, message: '请选择性别' }],
  category: [{ required: true, message: '请选择占卜事项' }],
};

const hexagramData = ref(null);
const casting = ref(false);
const ai = useAiStream();

const currentStep = computed(() => {
  if (ai.phase.value !== 'idle') {
    return 2;
  }
  return hexagramData.value ? 1 : 0;
});

const questionPlaceholder = computed(() => QUESTION_PLACEHOLDERS[formState.category] || '例如：下半年适合换工作吗？');

const genderLabel = computed(() => (formState.gender === 'girl' ? '女' : '男'));

const demandText = computed(() => {
  const question = formState.question.trim();
  return question ? `${formState.category}：${question}` : formState.category;
});

const dongyao = computed(() => hexagramData.value?.bengua?.dongyao || []);

const dongyaoText = computed(() => formatDongyao(dongyao.value));

const copyPrefix = computed(() => {
  if (!hexagramData.value) {
    return '';
  }
  return [
    `【六爻占卜】${demandText.value}`,
    `本卦：${hexagramData.value.bengua.gua}　变卦：${hexagramData.value.biangua.gua}`,
    `动爻：${dongyaoText.value}`,
  ].join('\n');
});

const selectCategory = (item) => {
  formState.category = item;
  if (formRef.value) {
    formRef.value.clearValidate(['category']);
  }
};

const onFinishFailed = () => {
  message.warning('请先选择性别和占卜事项');
};

// The out-in transition mounts the hexagram card only after the form has left
const onStepEntered = () => {
  if (hexagramData.value) {
    scrollToElement(hexagramRef.value);
  }
};

const castHexagram = async () => {
  casting.value = true;
  try {
    const { data } = await http.post('/zhanbu/cast_hexagram', {});
    if (data?.status === 'success' && data.hexagram_data) {
      hexagramData.value = data.hexagram_data;
      ai.reset();
    } else if (data?.status === 'limited') {
      message.warning(data.message || '今日次数已用完，请明天再试');
    } else {
      message.error('起卦失败，请稍后再试');
    }
  } catch (error) {
    console.error('castHexagram failed:', error);
    message.error(getErrorMessage(error, '起卦失败，请稍后再试'));
  } finally {
    casting.value = false;
  }
};

const analyzeHexagram = async () => {
  if (!hexagramData.value || ai.busy.value) {
    return;
  }
  const request = ai.start('/zhanbu/analyze_hexagram/stream', {
    gender: formState.gender,
    category: formState.category,
    question: formState.question.trim(),
    demand: demandText.value,
    hexagram_data: hexagramData.value,
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

const resetHexagram = () => {
  hexagramData.value = null;
  ai.reset();
  window.scrollTo({ top: 0, behavior: 'smooth' });
};
</script>

<style scoped>
/* ========== Steps ========== */
.steps {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0;
  margin: 0 0 36px;
  padding: 0;
  list-style: none;
}

.steps__item {
  display: flex;
  align-items: baseline;
  gap: 10px;
  color: var(--text-muted);
  opacity: 0.6;
  transition: color 0.4s var(--ease), opacity 0.4s var(--ease);
}

.steps__item + .steps__item::before {
  content: '';
  align-self: center;
  width: 56px;
  height: 1px;
  margin: 0 22px;
  background: var(--line);
}

.steps__numeral {
  font-family: var(--font-serif);
  font-size: 13px;
}

.steps__title {
  font-family: var(--font-serif);
  font-size: 14px;
  letter-spacing: 4px;
}

.steps__item.is-done {
  opacity: 1;
}

.steps__item.is-current {
  opacity: 1;
  color: var(--text);
}

.steps__item.is-current .steps__numeral {
  color: var(--accent);
}

.cast-tip {
  margin-bottom: 32px;
  padding: 16px 20px;
  border: none;
  border-left: 1px solid var(--accent);
  border-radius: 0;
  background: transparent;
}

.cast-tip :deep(.ant-alert-icon) {
  display: none;
}

.cast-tip :deep(.ant-alert-message) {
  font-family: var(--font-serif);
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 4px;
  color: var(--text);
}

.cast-tip :deep(.ant-alert-description) {
  font-size: 13px;
  line-height: 1.9;
  color: var(--text-muted);
}

/* ========== Hexagram pair ========== */
.hexagram-pair {
  display: flex;
  align-items: stretch;
  margin-bottom: 28px;
}

.hexagram-pair__arrow {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex: 0 0 auto;
  padding: 0 8px;
}

.hexagram-pair__arrow::before,
.hexagram-pair__arrow::after {
  content: '';
  width: 1px;
  height: 56px;
  background: var(--line);
}

.hexagram-pair__arrow span {
  font-family: var(--font-serif);
  font-size: 16px;
  letter-spacing: 2px;
  color: var(--accent);
}

.dongyao-info {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: center;
  gap: 8px 18px;
  padding: 18px 0;
  margin-bottom: 32px;
  border-top: 1px solid var(--line-soft);
  border-bottom: 1px solid var(--line-soft);
}

.dongyao-info__label {
  font-size: 12px;
  letter-spacing: 4px;
  color: var(--text-muted);
}

.dongyao-info__value {
  font-family: var(--font-serif);
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 3px;
  color: var(--cinnabar);
}

.dongyao-info__note {
  font-size: 12px;
  color: var(--text-muted);
}

.analysis-anchor {
  scroll-margin-top: calc(var(--header-height) + 16px);
}

@media (max-width: 640px) {
  .steps {
    margin-bottom: 22px;
  }

  .steps__item {
    gap: 6px;
  }

  .steps__item + .steps__item::before {
    width: 18px;
    margin: 0 10px;
  }

  .steps__title {
    font-size: 13px;
    letter-spacing: 2px;
  }

  .hexagram-pair {
    flex-direction: column;
  }

  .hexagram-pair__arrow {
    flex-direction: row;
    padding: 4px 0;
  }

  .hexagram-pair__arrow::before,
  .hexagram-pair__arrow::after {
    width: 48px;
    height: 1px;
  }
}
</style>
