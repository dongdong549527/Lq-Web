import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import MainLayout from '@/layout/MainLayout.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { public: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { public: true }
    },
    {
      path: '/',
      component: MainLayout,
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/HomeView.vue'),
        },
        {
          path: 'depots',
          name: 'depots',
          component: () => import('@/views/DepotList.vue'),
        },
        {
          path: 'granaries',
          name: 'granaries',
          component: () => import('@/views/GranaryList.vue'),
        },
        {
          path: 'users',
          name: 'users',
          component: () => import('@/views/UserList.vue'),
        },
      ]
    }
  ],
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  
  if (to.meta.public) {
    if (authStore.isAuthenticated) {
        return next('/');
    }
    return next();
  }

  if (!authStore.isAuthenticated) {
    return next('/login');
  }

  next();
});

export default router;
