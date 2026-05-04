import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';

// Oldalak importálása
import LoginPage from '@/pages/Login.page.vue';
import RegisterPage from '../pages/Register.page.vue';
import HomePage from '@/pages/Home.page.vue';
import BookListPage from '@/pages/BookList.page.vue';
import BookingListPage from '@/pages/BookingList.page.vue';
import ProfilePage from '../pages/Profile.page.vue';
import BookDetailsPage from '@/pages/BookDetails.page.vue';
import EditBookPage from '@/pages/EditBook.page.vue';

// Itt definiáljuk a routes tömböt - ez hiányzott a hibaüzeneted szerint
const routes = [
  { 
    path: '/login', 
    component: LoginPage, 
    meta: { public: true } 
  },
  { 
    path: '/register', 
    component: RegisterPage, 
    meta: { public: true } 
  },
  { 
    path: '/', 
    component: HomePage 
  },
  { 
    path: '/books', 
    component: BookListPage 
  },
  { 
    path: '/books/:id', 
    component: BookDetailsPage 
  },
  { 
    path: '/books/new', 
    component: EditBookPage
  },
  { 
    path: '/books/:id/edit', 
    component: EditBookPage 
  },
  { 
    path: '/bookings', 
    component: BookingListPage 
  },
  { 
    path: '/profile', 
    component: ProfilePage 
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const authStore = useAuthStore();
  if (!to.meta.public && !authStore.isAuthenticated) {
    return '/login';
  }
  return true;
});

export default router;