<template>
  <div class="page home-page">
    <!-- 首屏 -->
    <section class="hero">
      <p class="hero__verse hero__verse--side" aria-hidden="true">道可道　非常道</p>

      <div class="hero__title-block">
        <h1 class="hero__title">问天</h1>
        <span class="seal hero__seal" aria-hidden="true">问道</span>
      </div>
      <p class="hero__verse">玄之又玄　众妙之门</p>
      <div class="divider" aria-hidden="true"></div>

      <div class="hero__actions">
        <router-link :to="{ name: 'Bazi' }" class="hero-btn hero-btn--primary">排八字</router-link>
        <router-link :to="{ name: 'Gua' }" class="hero-btn hero-btn--ghost">起一卦</router-link>
      </div>
    </section>

    <!-- 二门 -->
    <section class="gates" aria-label="功能入口">
      <router-link
        v-for="gate in gates"
        :key="gate.route"
        :to="{ name: gate.route }"
        class="gate"
      >
        <span class="gate__numeral" aria-hidden="true">{{ gate.numeral }}</span>
        <h2 class="gate__title">{{ gate.title }}</h2>
        <p class="gate__keys">{{ gate.keys }}</p>
        <p class="gate__desc">{{ gate.desc }}</p>
        <span class="gate__enter">入<span aria-hidden="true">　→</span></span>
      </router-link>
    </section>

    <!-- 所本 -->
    <section class="tenets" aria-label="本站所本">
      <div v-for="tenet in tenets" :key="tenet.title" class="tenet">
        <h3 class="tenet__title">{{ tenet.title }}</h3>
        <p class="tenet__desc">{{ tenet.desc }}</p>
      </div>
    </section>

    <!-- 免责声明 -->
    <section class="disclaimer" aria-label="免责声明">
      <p>
        本站所有命理与占卜内容<strong>仅供娱乐参考</strong>，不构成任何建议，亦不可作为决策依据。
        请理性看待，切勿迷信——命运终究在自己手中。
      </p>
    </section>
  </div>
</template>

<script setup>
const gates = [
  {
    route: 'Bazi',
    numeral: '壹',
    title: '八字',
    keys: '四柱 · 五行 · 大运',
    desc: '以生辰立四柱，观五行之偏全、日主之强弱、大运之流转。',
  },
  {
    route: 'Gua',
    numeral: '贰',
    title: '六爻',
    keys: '起卦 · 动爻 · 变卦',
    desc: '三钱六掷，成卦观变。依朱子变占之法，取应占之辞。',
  },
];

const tenets = [
  {
    title: '以算为体',
    desc: '干支历法、藏干十神、旺衰喜用，皆由程序依古法推算，同一生辰，结果恒定。',
  },
  {
    title: '以经为据',
    desc: '解读只引《周易》《滴天髓》《穷通宝鉴》原文，有出处可查，不作杜撰。',
  },
  {
    title: '以人为本',
    desc: '吉凶之断，落于修身处事。知其所以然，而后知所进退。',
  },
];
</script>

<style scoped>
/* ========== Hero ========== */
.hero {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(78vh - var(--header-height));
  padding: 40px 16px 64px;
  text-align: center;
}

.hero__title-block {
  position: relative;
  display: inline-flex;
}

.hero__title {
  margin: 0;
  padding-left: 0.5em;
  font-family: var(--font-serif);
  font-size: 112px;
  font-weight: 600;
  line-height: 1.1;
  letter-spacing: 0.5em;
  color: var(--text);
}

/* Placed like a collector's seal at the lower right of a calligraphy work */
.hero__seal {
  position: absolute;
  right: -8px;
  bottom: 4px;
  width: 34px;
  height: 34px;
  font-size: 13px;
}

.hero__verse {
  margin-top: 28px;
  font-family: var(--font-serif);
  font-size: 16px;
  letter-spacing: 10px;
  color: var(--text-muted);
}

.hero__verse--side {
  position: absolute;
  top: 50%;
  right: 2%;
  margin: 0;
  writing-mode: vertical-rl;
  transform: translateY(-50%);
  font-size: 14px;
  letter-spacing: 14px;
  color: var(--text-muted);
  opacity: 0.6;
}

.hero__actions {
  display: flex;
  justify-content: center;
  gap: 18px;
  flex-wrap: wrap;
  margin-top: 48px;
}

.hero-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 156px;
  height: 50px;
  padding: 0 32px;
  border-radius: var(--radius);
  font-family: var(--font-serif);
  font-size: 17px;
  font-weight: 600;
  letter-spacing: 8px;
  text-decoration: none;
  transition: background 0.4s var(--ease), color 0.4s var(--ease), border-color 0.4s var(--ease);
}

.hero-btn--primary {
  background: var(--text);
  color: #11110f;
}

.hero-btn--ghost {
  border: 1px solid var(--line);
  color: var(--text-soft);
}

/* ========== Gates ========== */
.gates {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  border-top: 1px solid var(--line-soft);
  border-bottom: 1px solid var(--line-soft);
}

.gate {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 56px 48px;
  color: inherit;
  text-decoration: none;
  transition: background 0.5s var(--ease);
}

.gate + .gate {
  border-left: 1px solid var(--line-soft);
}

.gate__numeral {
  font-family: var(--font-serif);
  font-size: 14px;
  letter-spacing: 4px;
  color: var(--accent);
  margin-bottom: 20px;
}

.gate__title {
  font-family: var(--font-serif);
  font-size: 34px;
  font-weight: 600;
  letter-spacing: 12px;
  color: var(--text);
  margin-bottom: 10px;
}

.gate__keys {
  font-size: 13px;
  letter-spacing: 3px;
  color: var(--text-muted);
  margin-bottom: 22px;
}

.gate__desc {
  font-family: var(--font-serif);
  font-size: 15px;
  line-height: 2;
  color: var(--text-soft);
  margin-bottom: 32px;
}

.gate__enter {
  margin-top: auto;
  font-family: var(--font-serif);
  font-size: 14px;
  letter-spacing: 4px;
  color: var(--text-muted);
  transition: color 0.4s var(--ease), letter-spacing 0.4s var(--ease);
}

/* ========== Tenets ========== */
.tenets {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 40px;
  padding: 72px 0 64px;
}

.tenet__title {
  font-family: var(--font-serif);
  font-size: 17px;
  font-weight: 600;
  letter-spacing: 6px;
  color: var(--text);
  margin-bottom: 14px;
}

.tenet__desc {
  font-size: 13px;
  line-height: 2;
  color: var(--text-muted);
}

/* ========== Disclaimer ========== */
.disclaimer {
  max-width: 560px;
  margin: 0 auto;
  font-size: 12px;
  line-height: 2;
  letter-spacing: 1px;
  text-align: center;
  color: var(--text-muted);
}

.disclaimer strong {
  font-weight: 600;
  color: var(--text-soft);
}

/* ========== Interaction ========== */
@media (hover: hover) {
  .hero-btn--primary:hover {
    background: #fffaf0;
  }

  .hero-btn--ghost:hover {
    color: var(--text);
    border-color: rgba(236, 230, 218, 0.4);
  }

  .gate:hover {
    background: rgba(236, 230, 218, 0.02);
  }

  .gate:hover .gate__enter {
    color: var(--text);
    letter-spacing: 8px;
  }
}

/* ========== Responsive ========== */
@media (max-width: 960px) {
  .hero__verse--side {
    display: none;
  }
}

@media (max-width: 768px) {
  .hero {
    min-height: calc(70vh - var(--header-height));
    padding: 32px 8px 48px;
  }

  .hero__title {
    font-size: 72px;
  }

  .hero__seal {
    width: 28px;
    height: 28px;
    font-size: 11px;
    right: -4px;
  }

  .hero__verse {
    margin-top: 22px;
    font-size: 14px;
    letter-spacing: 6px;
  }

  .hero__actions {
    gap: 12px;
    margin-top: 36px;
    width: 100%;
    max-width: 360px;
  }

  .hero-btn {
    flex: 1 1 0;
    min-width: 0;
    height: 48px;
    padding: 0 12px;
    font-size: 16px;
    letter-spacing: 6px;
  }

  .gates {
    grid-template-columns: 1fr;
  }

  .gate {
    padding: 36px 8px;
  }

  .gate + .gate {
    border-left: none;
    border-top: 1px solid var(--line-soft);
  }

  .gate__title {
    font-size: 28px;
  }

  .gate__desc {
    margin-bottom: 20px;
  }

  .tenets {
    grid-template-columns: 1fr;
    gap: 28px;
    padding: 48px 8px 40px;
  }
}
</style>
