import MarkdownIt from 'markdown-it';

/** Raw HTML is disabled so model output can never inject markup into the page */
const md = new MarkdownIt({
  html: false,
  linkify: true,
  breaks: true,
});

/**
 * @param {string} source
 * @returns {string}
 */
export function renderMarkdown(source) {
  if (!source) {
    return '';
  }
  return md.render(String(source));
}
