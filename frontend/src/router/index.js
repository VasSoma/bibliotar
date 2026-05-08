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
import NotFoundPage from '@/pages/NotFound.page.vue'
import EditBookPage from '@/pages/EditBook.page.vue'
import { ROLES } from '@/consts/role.const'
import AccessDeniedPage from '@/pages/AccessDenied.page.vue'

const publicRoutes = [
  { path: '/login', name: 'login', component: LoginPage },
  { path: '/register', name: 'register', component: RegisterPage },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFoundPage },
]

const privateRoutes = [
  { path: '', name: 'home', component: HomePage, meta: { requiresAuth: true } },
  { path: '/books', name: 'books', component: BookListPage, meta: { requiresAuth: true } },
  { path: '/books/:id', name: 'book-details', component: BookDetailsPage, meta: { requiresAuth: true } },
  { path: '/books/new', name: 'book-new', component: EditBookPage, meta: { requiresAuth: true, roles: [ROLES.ADMIN] } },
  { path: '/books/:id/edit', name: 'book-edit', component: EditBookPage, meta: { requiresAuth: true, roles: [ROLES.ADMIN] } },
  { path: '/bookings', name: 'bookings', component: BookingListPage, meta: { requiresAuth: true } },
  { path: '/bookings/:id', name: 'booking-details', component: BookingDetailsPage, meta: { requiresAuth: true } },
  { path: '/profile', name: 'profile', component: ProfilePage, meta: { requiresAuth: true } },
  { path: '/access-denied', name: 'access-denied', component: AccessDeniedPage, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [...publicRoutes, ...privateRoutes],
})

router.beforeEach(async (to, from) => {
  const auth = useAuthStore()

  if (localStorage.getItem('token') && !auth.user) {
    await auth.fetchUser()
  }

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return '/login'
  }

  if (to.meta.roles && !auth.hasRole(to.meta.roles)) {
    return '/access-denied'
  }

  if (auth.isAuthenticated && publicRoutes.map((r) => r.path).includes(to.path)) {
    return '/books'
  }

  return true 
})

export default router