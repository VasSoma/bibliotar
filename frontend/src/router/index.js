import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ROLE_ADMIN, ROLE_LIBRARIAN, ROLE_USER } from '@/consts/role.const'

import LoginPage from '../pages/Login.page.vue'
import BookListPage from '../pages/BookList.page.vue'
/* import RegisterPage from '../pages/Register.page.vue'
import ProfilePage from '../pages/Profile.page.vue'

import BookDetailsPage from '../pages/BookDetails.page.vue'
import BookingListPage from '../pages/BookingList.page.vue'
import BookingDetailsPage from '../pages/BookingDetails.page.vue'
import EditBookPage from '@/pages/EditBook.page.vue'
import NotFoundPage from '@/pages/NotFound.page.vue'
 */
const publicRoutes = [
  {
    path: '/login',
    name: 'login',
    component: LoginPage,
  },
  /* {
    path: '/register',
    name: 'register',
    component: RegisterPage,
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundPage,
  }, */
]

const privateRoutes = [
   {
    path: '/books',
    name: 'books',
    component: BookListPage,
    meta: { requiresAuth: true, roles: [ROLE_USER, ROLE_LIBRARIAN, ROLE_ADMIN] },
  },/*
  {
    path: '/books/:id',
    name: 'book-details',
    component: BookDetailsPage,
    meta: { requiresAuth: true, roles: [ROLE_USER, ROLE_LIBRARIAN, ROLE_ADMIN] },
  },
  {
    path: '/books/new',
    name: 'book-new',
    component: EditBookPage,
    meta: { requiresAuth: true, roles: [ROLE_ADMIN] },
  },
  {
    path: '/books/:id/edit',
    name: 'book-edit',
    component: EditBookPage,
    meta: { requiresAuth: true, roles: [ROLE_ADMIN] },
  },
  {
    path: '/bookings',
    name: 'bookings',
    component: BookingListPage,
    meta: { requiresAuth: true, roles: [ROLE_USER, ROLE_LIBRARIAN, ROLE_ADMIN] },
  },
  {
    path: '/bookings/:id',
    name: 'booking-details',
    component: BookingDetailsPage,
    meta: { requiresAuth: true, roles: [ROLE_USER, ROLE_LIBRARIAN, ROLE_ADMIN] },
  },

  {
    path: '/profile',
    name: 'profile',
    component: ProfilePage,
    meta: { requiresAuth: true },
  }, */
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [...publicRoutes, ...privateRoutes],
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  // not logged in
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return next('/login')
  }

  // role check
  if (to.meta.roles && !auth.hasRole(to.meta.roles)) {
    return next('/unauthorized') // or 403 page
  }

  // go to home from public routes when user is authenticated
  if (auth.isAuthenticated && publicRoutes.map((r) => r.path).includes(to.path)) {
    next('/books')
  }

  next()
})

export default router