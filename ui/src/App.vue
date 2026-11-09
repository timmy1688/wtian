<template>
  <a-config-provider :locale="zhCN" :theme="themeConfig">
    <div class="app-container">
      <div class="backdrop" aria-hidden="true">
        <TaijiSymbol
          class="backdrop__taiji"
          :size="isMobile ? 560 : 1080"
          variant="line"
          bagua
          :spin="!isMobile"
        />
      </div>

      <header class="site-header">
        <div class="header-content">
          <router-link :to="{ name: 'Home' }" class="logo" aria-label="返回首页">
            <TaijiSymbol :size="isMobile ? 22 : 26" />
            <span class="logo__title">问天</span>
          </router-link>

          <nav v-if="!isMobile" class="desktop-nav" aria-label="主导航">
            <router-link
              v-for="item in navItems"
              :key="item.key"
              :to="{ name: item.route }"
              :class="['nav-item', { active: isActive(item.route) }]"
              :aria-current="isActive(item.route) ? 'page' : undefined"
            >
              {{ item.label }}
            </router-link>
          </nav>

          <a
            href="https://github.com/timmy1688/wtian"
            target="_blank"
            rel="noopener noreferrer"
            class="github-link"
            title="访问 GitHub 项目"
            aria-label="访问 GitHub 项目"
          >
            <GithubOutlined />
          </a>
        </div>
      </header>

      <main class="main-content">
        <div class="content-container">
          <router-view v-slot="{ Component }">
            <transition name="fade-slide" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </main>

      <footer class="site-footer">
        <div class="footer-content">
          <p class="footer-motto">道法自然</p>
          <p class="footer-note">
            内容仅供娱乐参考，请理性看待 ·
            <a href="https://github.com/timmy1688/wtian" target="_blank" rel="noopener noreferrer">开源</a>
          </p>
          <p class="footer-note footer-beian">
            <a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener noreferrer">{{ ICP_BEIAN }}</a>
          </p>
        </div>
      </footer>

      <!-- 移动端底部导航 -->
      <nav v-if="isMobile" class="tabbar" aria-label="底部导航">
        <router-link
          v-for="item in navItems"
          :key="item.key"
          :to="{ name: item.route }"
          :class="['tabbar__item', { active: isActive(item.route) }]"
          :aria-current="isActive(item.route) ? 'page' : undefined"
        >
          <span class="tabbar__glyph" aria-hidden="true">{{ item.glyph }}</span>
          <span class="tabbar__label">{{ item.shortLabel }}</span>
        </router-link>
      </nav>
    </div>
  </a-config-provider>
</template>

<script setup>
import { computed } from 'vue';
import { theme } from 'ant-design-vue';
import { GithubOutlined } from '@ant-design/icons-vue';
import { useRoute } from 'vue-router';
import { useWindowSize } from '@vueuse/core';
import zhCN from 'ant-design-vue/es/locale/zh_CN';
import TaijiSymbol from './components/common/TaijiSymbol.vue';

const MOBILE_BREAKPOINT = 768;
const ICP_BEIAN = '粤ICP备2025410144号';

// Keep in sync with the CSS variables in global.css
const themeConfig = {
  algorithm: theme.darkAlgorithm,
  token: {
    colorPrimary: '#c3a46e',
    colorLink: '#c3a46e',
    colorInfo: '#c3a46e',
    colorWarning: '#c3a46e',
    colorError: '#c0543d',
    colorText: '#ece6da',
    colorTextSecondary: '#b8b1a4',
    colorTextTertiary: '#7c766c',
    colorTextLightSolid: '#11110f',
    colorBorder: 'rgba(236, 230, 218, 0.16)',
    colorBorderSecondary: 'rgba(236, 230, 218, 0.08)',
    colorBgBase: '#0b0b0a',
    colorBgContainer: '#151513',
    colorBgElevated: '#1a1a17',
    borderRadius: 2,
    boxShadow: 'none',
    fontFamily: "'PingFang SC', 'HarmonyOS Sans SC', 'Noto Sans SC', 'Microsoft YaHei', system-ui, sans-serif",
  },
};

const route = useRoute();

const { width } = useWindowSize();
const isMobile = computed(() => width.value <= MOBILE_BREAKPOINT);

const navItems = [
  { key: 'home', label: '首页', shortLabel: '问天', glyph: '道', route: 'Home' },
  { key: 'bazi', label: '八字', shortLabel: '八字', glyph: '命', route: 'Bazi' },
  { key: 'gua', label: '六爻', shortLabel: '六爻', glyph: '卜', route: 'Gua' },
];

const isActive = (routeName) => route.name === routeName;
</script>

<style scoped>
.app-container {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding-bottom: calc(var(--tabbar-height) + env(safe-area-inset-bottom, 0px));
}

/* ========== Backdrop: ink darkness with one faint, slowly turning taiji ========== */
.backdrop {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
  background: radial-gradient(ellipse 70% 60% at 50% 30%, #141412 0%, var(--bg) 70%, #070706 100%);
}

.backdrop__taiji {
  position: absolute;
  top: 50%;
  left: 50%;
  margin: -540px 0 0 -540px;
  opacity: 0.07;
}

/* ========== Header ========== */
.site-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(11, 11, 10, 0.97);
  border-bottom: 1px solid var(--line-soft);
}

.header-content {
  max-width: 1100px;
  height: var(--header-height);
  margin: 0 auto;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 14px;
  text-decoration: none;
}

.logo__title {
  font-family: var(--font-serif);
  font-size: 20px;
  font-weight: 600;
  letter-spacing: 10px;
  color: var(--text);
}

.desktop-nav {
  display: flex;
  align-items: center;
  gap: 48px;
}

.nav-item {
  position: relative;
  padding: 6px 0;
  font-family: var(--font-serif);
  font-size: 15px;
  letter-spacing: 6px;
  color: var(--text-muted);
  text-decoration: none;
  transition: color 0.4s var(--ease);
}

.nav-item::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: -2px;
  width: 0;
  height: 1px;
  background: var(--accent);
  transform: translateX(-50%);
  transition: width 0.4s var(--ease);
}

.nav-item:hover {
  color: var(--text);
}

.nav-item.active {
  color: var(--text);
}

.nav-item.active::after {
  width: 16px;
}

.github-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  color: var(--text-muted);
  font-size: 16px;
  transition: color 0.3s var(--ease);
}

.github-link:hover {
  color: var(--text);
}

/* ========== Main ========== */
.main-content {
  position: relative;
  z-index: 1;
  flex: 1;
  padding: 56px 0 80px;
}

.content-container {
  max-width: 920px;
  margin: 0 auto;
  padding: 0 32px;
}

/* ========== Footer ========== */
.site-footer {
  position: relative;
  z-index: 1;
  border-top: 1px solid var(--line-soft);
}

.footer-content {
  max-width: 1100px;
  margin: 0 auto;
  padding: 36px 24px 32px;
  text-align: center;
}

.footer-motto {
  font-family: var(--font-serif);
  font-size: 15px;
  letter-spacing: 12px;
  color: var(--text-soft);
  margin-bottom: 12px;
}

.footer-note {
  font-size: 12px;
  letter-spacing: 1px;
  color: var(--text-muted);
}

.footer-note a {
  color: var(--text-soft);
  text-decoration: none;
}

.footer-note a:hover {
  color: var(--text);
}

.footer-beian {
  margin-top: 6px;
}

.footer-beian a {
  color: var(--text-muted);
}

/* ========== Mobile tab bar ========== */
.tabbar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  height: calc(var(--tabbar-height) + env(safe-area-inset-bottom, 0px));
  padding-bottom: env(safe-area-inset-bottom, 0px);
  background: rgba(11, 11, 10, 0.96);
  border-top: 1px solid var(--line-soft);
}

.tabbar__item {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  text-decoration: none;
  color: var(--text-muted);
  transition: color 0.3s var(--ease);
}

.tabbar__item::before {
  content: '';
  position: absolute;
  top: -1px;
  left: 50%;
  width: 0;
  height: 1px;
  background: var(--accent);
  transform: translateX(-50%);
  transition: width 0.3s var(--ease);
}

.tabbar__glyph {
  font-family: var(--font-serif);
  font-size: 19px;
  line-height: 1;
}

.tabbar__label {
  font-size: 11px;
  letter-spacing: 3px;
}

.tabbar__item.active {
  color: var(--text);
}

.tabbar__item.active::before {
  width: 24px;
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .header-content {
    padding: 0 18px;
  }

  .logo__title {
    font-size: 18px;
    letter-spacing: 8px;
  }

  .main-content {
    padding: 28px 0 40px;
  }

  .content-container {
    padding: 0 14px;
  }

  .footer-content {
    padding: 26px 16px 22px;
  }

  .backdrop__taiji {
    top: 18%;
    margin: -280px 0 0 -280px;
  }
}
</style>
