<template>
  <section class="panel">
    <div class="section-heading">
      <h2 class="section-heading__title">{{ title }}</h2>
      <span v-if="streaming" class="writing-hint" role="status">
        <span class="writing-hint__dot" aria-hidden="true"></span>
        推演中
      </span>
      <a-button v-else class="copy-btn" @click="handleCopy">
        <template #icon>
          <CheckOutlined v-if="copied" />
          <CopyOutlined v-else />
        </template>
        {{ copied ? '已复制' : '复制全文' }}
      </a-button>
    </div>
    <slot name="summary" />
    <article
      :class="['analysis-body', 'markdown-body', { 'analysis-body--streaming': streaming }]"
      :aria-busy="streaming"
      v-html="html"
    ></article>
    <p v-if="!streaming" class="analysis-disclaimer">以上内容由 AI 生成，仅供娱乐参考，请理性看待。</p>
  </section>
</template>

<script setup>
import { computed, onBeforeUnmount, ref } from 'vue';
import { message } from 'ant-design-vue';
import { CheckOutlined, CopyOutlined } from '@ant-design/icons-vue';
import { renderMarkdown } from '../../utils/markdown';
import { copyText } from '../../utils/dom';

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  content: {
    type: String,
    default: '',
  },
  // Plain-text prefix prepended to the copied content, e.g. the chart summary
  copyPrefix: {
    type: String,
    default: '',
  },
  // True while text is still arriving from the stream
  streaming: {
    type: Boolean,
    default: false,
  },
});

const COPIED_RESET_MS = 2000;

const html = computed(() => renderMarkdown(props.content));
const copied = ref(false);
let resetTimer = null;

const handleCopy = async () => {
  const text = props.copyPrefix ? `${props.copyPrefix}\n\n${props.content}` : props.content;
  try {
    await copyText(text);
    copied.value = true;
    message.success('已复制到剪贴板');
    window.clearTimeout(resetTimer);
    resetTimer = window.setTimeout(() => {
      copied.value = false;
    }, COPIED_RESET_MS);
  } catch (error) {
    console.error('Copy failed:', error);
    message.error('复制失败，请手动选择文本复制');
  }
};

onBeforeUnmount(() => {
  window.clearTimeout(resetTimer);
});
</script>

<style scoped>
.writing-hint {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  letter-spacing: 3px;
  color: var(--text-muted);
}

.writing-hint__dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--text-soft);
  animation: breathe 1.6s ease-in-out infinite;
}

.copy-btn.ant-btn {
  padding: 0;
  height: auto;
  border: none;
  background: transparent;
  font-size: 13px;
  letter-spacing: 2px;
  color: var(--text-muted);
}

.copy-btn.ant-btn:hover {
  color: var(--text);
  background: transparent;
}

.analysis-body {
  position: relative;
  max-width: 720px;
  margin: 0 auto;
}

.analysis-disclaimer {
  margin: 36px 0 0;
  padding-top: 18px;
  border-top: 1px solid var(--line-soft);
  font-size: 12px;
  letter-spacing: 1px;
  color: var(--text-muted);
  text-align: center;
}
</style>
