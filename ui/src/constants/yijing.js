export const TRIGRAM_INFO = {
  乾: { symbol: '☰', nature: '天' },
  兑: { symbol: '☱', nature: '泽' },
  离: { symbol: '☲', nature: '火' },
  震: { symbol: '☳', nature: '雷' },
  巽: { symbol: '☴', nature: '风' },
  坎: { symbol: '☵', nature: '水' },
  艮: { symbol: '☶', nature: '山' },
  坤: { symbol: '☷', nature: '地' },
};

/** Index 0 is the bottom line (初爻) */
export const YAO_POSITION_LABELS = ['初爻', '二爻', '三爻', '四爻', '五爻', '上爻'];

export const GUA_DEMAND_OPTIONS = ['事业', '爱情', '财运', '健康', '学业', '其他'];

/**
 * @param {string} name trigram name such as "坤"
 * @returns {string} e.g. "坤☷ (地)"
 */
export function formatTrigram(name) {
  const info = TRIGRAM_INFO[name];
  if (!info) {
    return name || '-';
  }
  return `${name}${info.symbol} (${info.nature})`;
}

/**
 * @param {number[]} positions 1-based moving line positions
 * @returns {string}
 */
export function formatDongyao(positions) {
  if (!Array.isArray(positions) || positions.length === 0) {
    return '无动爻';
  }
  return positions
    .map((position) => YAO_POSITION_LABELS[position - 1] || `第${position}爻`)
    .join('、');
}
