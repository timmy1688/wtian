import { createRouter, createWebHistory } from 'vue-router';
import Bazi from '../components/BaziView.vue';
import Gua from '../components/GuaView.vue';
import Home from '../components/HomeView.vue';
import Ops from '../components/OpsView.vue';

const SITE_NAME = '问天';

const routes = [
  {
    path: '/',
    redirect: { name: 'Home' },
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { title: '首页' },
  },
  {
    path: '/bazi',
    name: 'Bazi',
    component: Bazi,
    meta: { title: '八字排盘' },
  },
  {
    path: '/gua',
    name: 'Gua',
    component: Gua,
    meta: { title: '六爻占卜' },
  },
  {
    path: '/ops',
    name: 'Ops',
    component: Ops,
    meta: { title: '记数' },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: { name: 'Home' },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    return { top: 0 };
  },
});

const PAGE_BEACON = { Home: 'home', Bazi: 'bazi', Gua: 'gua' };

router.afterEach((to) => {
  const pageTitle = to.meta && to.meta.title;
  document.title = pageTitle ? `${pageTitle} - ${SITE_NAME}` : SITE_NAME;
  const page = PAGE_BEACON[to.name];
  if (!page) {
    return;
  }
  const body = JSON.stringify({ page });
  const url = '/api/ops/visit';
  if (navigator.sendBeacon) {
    navigator.sendBeacon(url, new Blob([body], { type: 'application/json' }));
    return;
  }
  fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body,
    keepalive: true,
  }).catch(() => {});
});

export default router;
