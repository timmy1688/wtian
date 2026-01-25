<template>
  <div class="app-container">
    <!-- 导航栏 -->
    <header class="modern-header">
      <div class="header-content">
        <div class="logo-section" @click="goToRoute('Home')">
          <div class="logo-icon">☯</div>
          <div class="logo-text">
            <div class="logo-title">问天易经</div>
            <div class="logo-subtitle">AI智能体</div>
          </div>
        </div>
        
        <!-- 桌面端导航 -->
        <nav v-if="!isMobile" class="desktop-nav">
          <a
            v-for="item in navItems"
            :key="item.key"
            :class="['nav-item', { active: isActive(item.key) }]"
            @click="goToRoute(item.route)"
          >
            <component :is="item.icon" class="nav-icon" />
            <span>{{ item.label }}</span>
          </a>
        </nav>

        <div class="header-actions">
          <!-- GitHub 链接 -->
          <a
            href="https://github.com/timmy1688/wtian"
            target="_blank"
            rel="noopener noreferrer"
            class="github-link"
            title="访问 GitHub 项目"
          >
            <GithubOutlined />
          </a>
          
          <!-- 移动端菜单按钮 -->
          <a-button
            v-if="isMobile"
            class="menu-toggle"
            type="text"
            @click="toggleDrawer"
          >
            <MenuOutlined />
          </a-button>
        </div>
      </div>
    </header>

    <!-- 移动端抽屉菜单 -->
    <a-drawer
      title="导航菜单"
      placement="right"
      :visible="drawerVisible"
      @close="toggleDrawer"
      :bodyStyle="{ padding: 0 }"
    >
      <div class="mobile-menu">
        <a
          v-for="item in navItems"
          :key="item.key"
          :class="['mobile-nav-item', { active: isActive(item.key) }]"
          @click="handleMenuClick(item.route)"
        >
          <component :is="item.icon" class="mobile-nav-icon" />
          <span>{{ item.label }}</span>
        </a>
      </div>
    </a-drawer>

    <!-- 主内容区 -->
    <main class="main-content">
      <div class="content-container">
        <router-view v-slot="{ Component }">
          <transition name="fade-slide" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="modern-footer">
      <div class="footer-content">
        <div class="footer-info">
          <p class="footer-title">问天易经AI - 让千年智慧遇见现代科技</p>
          <p class="footer-description">
            融合传统易经算法与大语言模型，为您提供专业的命理分析服务
          </p>
        </div>
        <div class="footer-links">
          <a href="https://github.com/timmy1688/wtian" target="_blank" rel="noopener noreferrer">
            <GithubOutlined /> GitHub
          </a>
        </div>
        <div class="footer-copyright">
          © 2024-2026 问天易经AI. All rights reserved.
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import {
  HomeOutlined,
  CalculatorOutlined,
  CompassOutlined,
  MenuOutlined,
  GithubOutlined,
} from '@ant-design/icons-vue';
import { useRouter, useRoute } from 'vue-router';
import { useWindowSize } from '@vueuse/core';

const router = useRouter();
const route = useRoute();

// 检测屏幕是否为移动端
const { width } = useWindowSize();
const isMobile = computed(() => width.value <= 768);

// 导航菜单项
const navItems = [
  { key: 'home', label: '首页', icon: HomeOutlined, route: 'Home' },
  { key: 'bazi', label: '八字测算', icon: CalculatorOutlined, route: 'Bazi' },
  { key: 'gua', label: '64卦占卜', icon: CompassOutlined, route: 'Gua' },
];

// 控制抽屉显示
const drawerVisible = ref(false);
const toggleDrawer = () => {
  drawerVisible.value = !drawerVisible.value;
};

// 判断当前路由是否激活
const isActive = (key) => {
  const routeName = route.name?.toLowerCase() || 'home';
  return routeName === key;
};

// 路由跳转
const goToRoute = (routeName) => {
  router.push({ name: routeName });
  if (isMobile.value) {
    drawerVisible.value = false;
  }
};

// 处理移动端菜单点击
const handleMenuClick = (routeName) => {
  goToRoute(routeName);
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
}

.app-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.05) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
  pointer-events: none;
}

/* ========== 导航栏 ========== */
.modern-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  transition: all 0.3s ease;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.logo-section:hover {
  transform: translateY(-2px);
}

.logo-icon {
  font-size: 36px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.2;
}

.logo-subtitle {
  font-size: 11px;
  color: #999;
  font-weight: 500;
  letter-spacing: 1px;
}

.desktop-nav {
  display: flex;
  gap: 8px;
  align-items: center;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 500;
  color: #555;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.nav-item:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.nav-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.nav-icon {
  font-size: 18px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.github-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: linear-gradient(135deg, #24292e 0%, #1a1a1a 100%);
  color: white;
  font-size: 20px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.github-link:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
}

.menu-toggle {
  color: #667eea;
  font-size: 24px;
  border: none;
}

/* ========== 移动端菜单 ========== */
.mobile-menu {
  display: flex;
  flex-direction: column;
  padding: 8px;
}

.mobile-nav-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  margin-bottom: 8px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 500;
  color: #555;
  cursor: pointer;
  transition: all 0.3s ease;
}

.mobile-nav-item:hover,
.mobile-nav-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transform: translateX(8px);
}

.mobile-nav-icon {
  font-size: 20px;
}

/* ========== 主内容区 ========== */
.main-content {
  flex: 1;
  position: relative;
  z-index: 1;
  padding: 32px 0;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* ========== 页面过渡动画 ========== */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* ========== 页脚 ========== */
.modern-footer {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  z-index: 1;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 24px 24px;
  text-align: center;
}

.footer-info {
  margin-bottom: 20px;
}

.footer-title {
  font-size: 18px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
}

.footer-description {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

.footer-links {
  margin-bottom: 16px;
}

.footer-links a {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.footer-links a:hover {
  color: #764ba2;
  transform: translateY(-2px);
}

.footer-copyright {
  font-size: 13px;
  color: #999;
  padding-top: 16px;
  border-top: 1px solid #eee;
}

/* ========== 响应式设计 ========== */
@media (max-width: 768px) {
  .header-content {
    height: 60px;
    padding: 0 16px;
  }

  .logo-icon {
    font-size: 28px;
  }

  .logo-title {
    font-size: 16px;
  }

  .logo-subtitle {
    font-size: 10px;
  }

  .github-link {
    width: 36px;
    height: 36px;
    font-size: 18px;
  }

  .main-content {
    padding: 20px 0;
  }

  .content-container {
    padding: 0 16px;
  }

  .footer-content {
    padding: 24px 16px 16px;
  }

  .footer-title {
    font-size: 16px;
  }

  .footer-description {
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .logo-section {
    gap: 8px;
  }

  .logo-icon {
    font-size: 24px;
  }

  .logo-title {
    font-size: 14px;
  }

  .logo-subtitle {
    display: none;
  }

  .content-container {
    padding: 0 12px;
  }
}
</style>
