import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Oldalak importálása
import LoginPage from '@/pages/Login.page.vue'
import RegisterPage from '../pages/Register.page.vue'
import HomePage from '@/pages/Home.page.vue'
import BookListPage from '@/pages/BookList.page.vue'
import BookingListPage from '@/pages/BookingList.page.vue'
import ProfilePage from '../pages/Profile.page.vue'
import BookDetailsPage from '@/pages/BookDetails.page.vue'
import BookingDetailsPage from '@/pages/BookingDetails.page.vue'
import NotFoundPagePage from '@/pages/NotFoundPage.page.vue'
import EditBookPage from '@/pages/EditBook.page.vue'
import { ROLES } from '@/consts/role.const'
import AccessDeniedPage from '@/pages/AccessDenied.page.vue'

const publicRoutes = [
  {
    path: '/login',
    name: 'login',
    component: LoginPage,
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage,
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundPagePage,
  },
]

const privateRoutes = [
  {
    path: '',
    name: 'home',
    component: HomePage,
    meta: { requiresAuth: true },
  },
  {
    path: '/books',
    name: 'books',
    component: BookListPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/books/:id',
    name: 'book-details',
    component: BookDetailsPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/books/new',
    name: 'book-new',
    component: EditBookPage,
    meta: { requiresAuth: true, roles: [ROLES.ADMIN] },
  },
  {
    path: '/books/:id/edit',
    name: 'book-edit',
    component: EditBookPage,
    meta: { requiresAuth: true, roles: [ROLES.ADMIN] },
  },
  {
    path: '/bookings',
    name: 'bookings',
    component: BookingListPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/bookings/:id',
    name: 'booking-details',
    component: BookingDetailsPage,
    meta: { requiresAuth: true },
  },

  {
    path: '/profile',
    name: 'profile',
    component: ProfilePage,
    meta: { requiresAuth: true },
  },
  {
    path: '/access-denied',
    name: 'access-denied',
    component: AccessDeniedPage,
    meta: { requiresAuth: true },
  },
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
    return next('/access-denied') // or 403 page
  }

  // go to home from public routes when user is authenticated
  if (auth.isAuthenticated && publicRoutes.map((r) => r.path).includes(to.path)) {
    next('/books')
  }

  next()
})

export default router
