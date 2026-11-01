export const PILLAR_NAMES = ['年柱', '月柱', '日柱', '时柱'];

export const WUXING_ORDER = ['木', '火', '土', '金', '水'];

/** Muted mineral pigments: 石绿, 朱砂, 赭石, 泥金, 黛青 */
export const WUXING_COLORS = {
  木: '#7f9c7a',
  火: '#c0614b',
  土: '#a88660',
  金: '#cbb994',
  水: '#7590a8',
};

export const GAN_WUXING = {
  甲: '木', 乙: '木',
  丙: '火', 丁: '火',
  戊: '土', 己: '土',
  庚: '金', 辛: '金',
  壬: '水', 癸: '水',
};

export const ZHI_WUXING = {
  子: '水', 亥: '水',
  寅: '木', 卯: '木',
  巳: '火', 午: '火',
  丑: '土', 辰: '土', 未: '土', 戌: '土',
  申: '金', 酉: '金',
};

/**
 * Each value is a representative hour inside the 时辰 range, matching
 * the backend `get_shichen` mapping. 早子时/晚子时 are split because the
 * day pillar differs between 00:xx and 23:xx.
 */
export const SHICHEN_OPTIONS = [
  { value: 0, label: '早子时 (00:00-00:59)' },
  { value: 2, label: '丑时 (01:00-02:59)' },
  { value: 4, label: '寅时 (03:00-04:59)' },
  { value: 6, label: '卯时 (05:00-06:59)' },
  { value: 8, label: '辰时 (07:00-08:59)' },
  { value: 10, label: '巳时 (09:00-10:59)' },
  { value: 12, label: '午时 (11:00-12:59)' },
  { value: 14, label: '未时 (13:00-14:59)' },
  { value: 16, label: '申时 (15:00-16:59)' },
  { value: 18, label: '酉时 (17:00-18:59)' },
  { value: 20, label: '戌时 (19:00-20:59)' },
  { value: 22, label: '亥时 (21:00-22:59)' },
  { value: 23, label: '晚子时 (23:00-23:59)' },
];

export const BAZI_DEMAND_OPTIONS = ['综合运势', '事业', '财运', '感情', '健康', '学业'];

/** Total characters across the four pillars (4 stems + 4 branches) */
export const BAZI_CHAR_COUNT = 8;
