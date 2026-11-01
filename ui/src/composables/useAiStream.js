import { computed, onBeforeUnmount, ref } from 'vue';
import { postStream, StreamError } from '../api/stream';
import { getServerMessage } from '../api/request';

/**
 * @typedef {'idle' | 'waiting' | 'streaming' | 'done'} StreamPhase
 * - waiting: request sent, no text yet
 * - streaming: text is arriving
 * - done: finished successfully
 */

/**
 * Reactive wrapper around postStream for AI analysis panels.
 * Text chunks are batched per animation frame so markdown is not re-rendered
 * for every token.
 */
export function useAiStream() {
  /** @type {import('vue').Ref<StreamPhase>} */
  const phase = ref('idle');
  const content = ref('');

  let controller = null;
  let pending = '';
  let frameId = 0;

  const flush = () => {
    frameId = 0;
    if (pending) {
      content.value += pending;
      pending = '';
    }
  };

  const scheduleFlush = () => {
    if (!frameId) {
      frameId = window.requestAnimationFrame(flush);
    }
  };

  const cancelFlush = () => {
    if (frameId) {
      window.cancelAnimationFrame(frameId);
      frameId = 0;
    }
  };

  const reset = () => {
    controller?.abort();
    controller = null;
    cancelFlush();
    pending = '';
    content.value = '';
    phase.value = 'idle';
  };

  /**
   * @param {string} path
   * @param {object} body
   * @returns {Promise<{ ok: true } | { ok: false, data?: object, message: string, aborted?: boolean }>}
   */
  const start = async (path, body) => {
    reset();
    const current = new AbortController();
    controller = current;
    phase.value = 'waiting';

    try {
      const outcome = await postStream(path, body, {
        signal: current.signal,
        onDelta: (text) => {
          if (phase.value === 'waiting') {
            phase.value = 'streaming';
          }
          pending += text;
          scheduleFlush();
        },
      });
      cancelFlush();
      flush();

      if (outcome.type === 'json') {
        const message = getServerMessage(outcome.data) || '请求未被受理，请稍后再试';
        content.value = '';
        phase.value = 'idle';
        return { ok: false, data: outcome.data, message };
      }
      phase.value = 'done';
      return { ok: true };
    } catch (error) {
      cancelFlush();
      const aborted = error?.name === 'AbortError';
      if (controller === current) {
        content.value = '';
        phase.value = 'idle';
      }
      const message = error instanceof StreamError ? error.message : '解读失败，请稍后再试';
      return { ok: false, aborted, message };
    } finally {
      if (controller === current) {
        controller = null;
      }
    }
  };

  onBeforeUnmount(reset);

  return {
    phase,
    content,
    busy: computed(() => phase.value === 'waiting' || phase.value === 'streaming'),
    start,
    reset,
  };
}
