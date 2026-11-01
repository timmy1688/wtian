import { createRouter, createWebHistory } from 'vue-router';
import Bazi from '../components/BaziView.vue';
import Gua from '../components/GuaView.vue';
import Home from '../components/HomeView.vue';

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

router.afterEach((to) => {
  const pageTitle = to.meta && to.meta.title;
  document.title = pageTitle ? `${pageTitle} - ${SITE_NAME}` : SITE_NAME;
});

export default router;
