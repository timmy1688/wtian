/**
 * Copy text to clipboard, falling back to execCommand on insecure origins.
 * @param {string} text
 * @returns {Promise<void>}
 */
export async function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text);
    return;
  }
  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.setAttribute('readonly', '');
  textarea.style.position = 'fixed';
  textarea.style.opacity = '0';
  document.body.appendChild(textarea);
  textarea.select();
  const succeeded = document.execCommand('copy');
  document.body.removeChild(textarea);
  if (!succeeded) {
    throw new Error('Copy command was rejected');
  }
}

/**
 * Smoothly scroll an element into view; offset is handled by CSS scroll-margin-top.
 * @param {HTMLElement | null | undefined} el
 */
export function scrollToElement(el) {
  if (!el || typeof el.scrollIntoView !== 'function') {
    return;
  }
  el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/** @returns {boolean} */
export function isTouchDevice() {
  return typeof window !== 'undefined'
    && typeof window.matchMedia === 'function'
    && window.matchMedia('(pointer: coarse)').matches;
}
