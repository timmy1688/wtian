import { API_BASE_URL } from './config';

/** Abort when the server sends nothing for this long (covers slow first token) */
const IDLE_TIMEOUT_MS = 60000;

export class StreamError extends Error {
  /**
   * @param {string} message user-facing message
   * @param {{ status?: number, payload?: object }} [detail]
   */
  constructor(message, detail = {}) {
    super(message);
    this.name = 'StreamError';
    this.status = detail.status;
    this.payload = detail.payload;
  }
}

/**
 * Map an HTTP status to a user-facing message.
 * @param {number} status
 * @returns {string}
 */
function statusMessage(status) {
  if (status === 422 || status === 400) {
    return '输入信息格式有误，请检查后重试';
  }
  if (status === 429) {
    return '请求过于频繁，请稍后再试';
  }
  return '服务器繁忙，请稍后再试';
}

/**
 * Parse SSE frames out of the buffer and dispatch them.
 * @param {string} buffer
 * @param {(event: object) => void} onEvent
 * @returns {string} unconsumed remainder
 */
function drainFrames(buffer, onEvent) {
  const frames = buffer.split(/\r?\n\r?\n/);
  const rest = frames.pop() ?? '';
  frames.forEach((frame) => {
    const data = frame
      .split(/\r?\n/)
      .filter((line) => line.startsWith('data:'))
      .map((line) => line.slice(5).trimStart())
      .join('\n');
    if (!data) {
      return;
    }
    try {
      onEvent(JSON.parse(data));
    } catch (error) {
      console.warn('Malformed SSE frame ignored:', data);
    }
  });
  return rest;
}

/**
 * POST a JSON body and consume a Server-Sent Events response.
 *
 * The backend answers with plain JSON instead of a stream when the request is
 * rejected before generation (rate limit, validation); that JSON is returned
 * as `{ type: 'json', data }` so callers can show the server message.
 *
 * @param {string} path API path such as "/bazi/fenxi/stream"
 * @param {object} body
 * @param {{ onDelta: (text: string) => void, signal?: AbortSignal }} options
 * @returns {Promise<{ type: 'done' } | { type: 'json', data: object }>}
 */
export async function postStream(path, body, { onDelta, signal } = {}) {
  const controller = new AbortController();
  let idleTimer = null;
  let timedOut = false;
  const resetIdle = () => {
    window.clearTimeout(idleTimer);
    idleTimer = window.setTimeout(() => {
      timedOut = true;
      controller.abort();
    }, IDLE_TIMEOUT_MS);
  };
  const forwardAbort = () => controller.abort();
  signal?.addEventListener('abort', forwardAbort);

  try {
    resetIdle();
    let response;
    try {
      response = await fetch(`${API_BASE_URL}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'text/event-stream' },
        body: JSON.stringify(body),
        signal: controller.signal,
      });
    } catch (error) {
      if (timedOut) {
        throw new StreamError('请求超时，AI 可能正在忙碌，请稍后重试');
      }
      if (error.name === 'AbortError') {
        throw error;
      }
      throw new StreamError('网络连接异常，请检查网络后重试');
    }

    if (!response.ok) {
      throw new StreamError(statusMessage(response.status), { status: response.status });
    }

    const contentType = response.headers.get('content-type') || '';
    if (!contentType.includes('text/event-stream')) {
      return { type: 'json', data: await response.json() };
    }
    if (!response.body) {
      throw new StreamError('当前浏览器不支持流式输出，请升级浏览器后重试');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';
    let finished = false;
    let serverError = null;

    const handleEvent = (event) => {
      if (event.type === 'delta' && typeof event.text === 'string') {
        onDelta?.(event.text);
      } else if (event.type === 'done') {
        finished = true;
      } else if (event.type === 'error') {
        serverError = event.message || 'AI 解读服务暂时不可用，请稍后再试';
      }
    };

    try {
      while (!finished && !serverError) {
        const { value, done } = await reader.read();
        if (done) {
          break;
        }
        resetIdle();
        buffer = drainFrames(buffer + decoder.decode(value, { stream: true }), handleEvent);
      }
      buffer = drainFrames(`${buffer}${decoder.decode()}\n\n`, handleEvent);
    } catch (error) {
      if (timedOut) {
        throw new StreamError('AI 响应中断（超时），请稍后重试');
      }
      if (error.name === 'AbortError') {
        throw error;
      }
      throw new StreamError('连接中断，请稍后重试');
    } finally {
      reader.cancel().catch(() => {});
    }

    if (serverError) {
      throw new StreamError(serverError);
    }
    if (!finished) {
      throw new StreamError('AI 响应不完整，请稍后重试');
    }
    return { type: 'done' };
  } finally {
    window.clearTimeout(idleTimer);
    signal?.removeEventListener('abort', forwardAbort);
  }
}
