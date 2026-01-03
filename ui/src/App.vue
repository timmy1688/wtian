<template>
  <a-layout class="layout">
    <a-layout-header class="header">
      <div class="logo">问天易经AI</div>
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
      <!-- 移动端汉堡菜单按钮 -->
      <a-button
        class="menu-toggle"
        type="text"
        @click="toggleDrawer"
        v-if="isMobile"
      >
        <MenuOutlined />
      </a-button>
      <!-- 桌面端水平菜单 -->
      <a-menu
        v-if="!isMobile"
        v-model:selectedKeys="current"
        theme="dark"
        mode="horizontal"
        :style="{ lineHeight: '64px' }"
        class="transparent-menu"
      >
        <a-menu-item key="home" @click="goToRoute('Home')">
          <template #icon><HomeOutlined /></template>
          首页
        </a-menu-item>
        <a-menu-item key="bazi" @click="goToRoute('Bazi')">
          <template #icon><CalculatorOutlined /></template>
          八字测算
        </a-menu-item>
        <a-menu-item key="guagua" @click="goToRoute('Gua')">
          <template #icon><CompassOutlined /></template>
          64卦占卜
        </a-menu-item>
      </a-menu>
      <!-- 移动端抽屉菜单 -->
      <a-drawer
        title="菜单"
        placement="right"
        :visible="drawerVisible"
        @close="toggleDrawer"
        class="mobile-menu"
      >
        <a-menu
          v-model:selectedKeys="current"
          mode="vertical"
          theme="light"
          @click="handleMenuClick"
        >
          <a-menu-item key="home">
            <HomeOutlined />
            首页
          </a-menu-item>
          <a-menu-item key="bazi">
            <CalculatorOutlined />
            八字测算
          </a-menu-item>
          <a-menu-item key="guagua">
            <CompassOutlined />
            64卦占卜
          </a-menu-item>
        </a-menu>
      </a-drawer>
    </a-layout-header>
    <a-layout-content class="content">
      <a-breadcrumb style="margin: 16px 0; font-size: 14px;">
        <a-breadcrumb-item>Home</a-breadcrumb-item>
        <a-breadcrumb-item>{{ route.name }}</a-breadcrumb-item>
      </a-breadcrumb>
      <div class="content-wrapper">
        <router-view />
      </div>
    </a-layout-content>
    <a-layout-footer class="footer">
      Your Footer Information Here
    </a-layout-footer>
  </a-layout>
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

// 控制抽屉显示
const drawerVisible = ref(false);
const toggleDrawer = () => {
  drawerVisible.value = !drawerVisible.value;
};

// 菜单选中状态
const current = computed(() => [route.name?.toLowerCase() || 'home']);

// 路由跳转
const goToRoute = (routeName) => {
  router.push({ name: routeName });
  if (isMobile.value) {
    drawerVisible.value = false; // 移动端选择后关闭抽屉
  }
};

// 处理抽屉菜单点击
const handleMenuClick = ({ key }) => {
  const routeMap = {
    home: 'Home',
    bazi: 'Bazi',
    guagua: 'Gua',
  };
  goToRoute(routeMap[key]);
};
</script>

<style scoped>
.layout {
  min-height: 100vh;
  background: #f0f2f5;
}

.header {
  background: linear-gradient(90deg, #1e3a8a, #3b82f6);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
}

.logo {
  color: white;
  font-size: 22px;
  font-weight: bold;
  line-height: 31px;
  margin: 16px 24px 16px 0;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.github-link {
  color: rgba(255, 255, 255, 0.8);
  font-size: 20px;
  margin-right: 16px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.github-link:hover {
  color: white;
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.transparent-menu {
  background: transparent !important;
  border-bottom: none;
  flex: 1;
}

.transparent-menu .ant-menu-item {
  color: rgba(255, 255, 255, 0.9);
  font-size: 16px;
  transition: all 0.3s ease;
}

.transparent-menu .ant-menu-item:hover {
  color: white;
  background: rgba(255, 255, 255, 0.15) !important;
}

.transparent-menu .ant-menu-item-selected {
  color: white !important;
  background: rgba(255, 255, 255, 0.2) !important;
  border-bottom: 2px solid white;
}

.menu-toggle {
  color: white;
  font-size: 20px;
}

.content {
  padding: 0 50px;
  margin-top: 24px;
}

.content-wrapper {
  background: #ffffff;
  padding: 32px;
  min-height: 280px;
  margin: 0 50px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.3s ease;
}

.content-wrapper:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.footer {
  text-align: center;
  background: #ffffff;
  color: #666;
  padding: 24px 50px;
  font-size: 14px;
  border-top: 1px solid #e8e8e8;
}

@media (max-width: 768px) {
  .content {
    padding: 0;
  }

  .content-wrapper {
    margin: 0;
    border-radius: 0;
    box-shadow: none;
  }

  .header {
    padding: 0 16px;
  }

  .logo {
    font-size: 18px;
    margin: 16px 16px 16px 0;
  }

  .github-link {
    margin-right: 8px;
    width: 36px;
    height: 36px;
    font-size: 18px;
  }

  .footer {
    padding: 16px;
  }
}

[data-theme='dark'] .layout {
  background: #1f1f1f;
}

[data-theme='dark'] .content-wrapper {
  background: #2d2d2d;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

[data-theme='dark'] .footer {
  background: #2d2d2d;
  color: #aaa;
  border-top: 1px solid #444;
}
</style>
