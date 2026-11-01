import axios from 'axios';
import { API_BASE_URL } from './config';

/** LLM analysis can take a while, so the timeout is intentionally generous */
const http = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
});

/**
 * Convert an axios error into a user-facing message.
 * @param {unknown} error
 * @param {string} fallback
 * @returns {string}
 */
export function getErrorMessage(error, fallback = '请求失败，请稍后再试') {
  if (!error || typeof error !== 'object') {
    return fallback;
  }
  if (error.code === 'ECONNABORTED') {
    return '请求超时，AI 可能正在忙碌，请稍后重试';
  }
  if (!error.response) {
    return '网络连接异常，请检查网络后重试';
  }
  const { status } = error.response;
  if (status === 422) {
    return '输入信息格式有误，请检查后重试';
  }
  if (status === 429) {
    return '请求过于频繁，请稍后再试';
  }
  if (status >= 500) {
    return '服务器繁忙，请稍后再试';
  }
  return fallback;
}

/**
 * Read the message from a business-level failure body.
 * The backend reports validation errors as HTTP 200 with `{ status: 'Failed', err_msg }`,
 * where err_msg is a string (HTTPException) or `{ msg }` (request validation).
 * @param {object} data
 * @returns {string}
 */
export function getServerMessage(data) {
  if (!data || typeof data !== 'object') {
    return '';
  }
  if (typeof data.message === 'string' && data.message) {
    return data.message;
  }
  const errMsg = data.err_msg;
  if (typeof errMsg === 'string') {
    return errMsg;
  }
  return errMsg?.msg || '';
}

export default http;
