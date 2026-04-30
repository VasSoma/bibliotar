import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import Home from '../pages/Home.page.vue';
import Login from '../pages/Login.page.vue';
import Profile from '../pages/Profile.page.vue';
import Books from '../pages/Books.page.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/books', component: Books },
  { 
    path: '/profile', 
    component: Profile,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;