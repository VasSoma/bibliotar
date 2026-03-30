import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../pages/Home.page.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../pages/Login.page.vue'),
    },
    {
      path: '/books',
      name: 'books',
      component: () => import('../pages/Books.page.vue'),
    },
  ],
})

export default router
