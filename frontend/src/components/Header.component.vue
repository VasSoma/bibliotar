<script setup>
import { ROLE_ADMIN, ROLE_LIBRARIAN, ROLE_USER } from '@/consts/role.const'
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'

const auth = useAuthStore()

const MENU_ITEMS = [
  { label: 'List of books', route: 'books', roles: [ROLE_USER, ROLE_LIBRARIAN, ROLE_ADMIN] },
 // { label: 'List of bookings', route: 'bookings', roles: [ROLE_USER, ROLE_LIBRARIAN, ROLE_ADMIN] },
 // { label: 'Profile', route: 'profile', roles: [ROLE_USER, ROLE_LIBRARIAN, ROLE_ADMIN] },
  { label: 'Logout', handler: () => auth.logout() },
]

const availableMenuItems = computed(() => MENU_ITEMS.filter((item) => auth.hasRole(item.roles)))
</script>

<template>
  <div v-if="auth.isAuthenticated" class="menu-container">
    <div v-for="item in availableMenuItems" :key="item.label">
      <RouterLink
        v-if="'route' in item"
        :to="{ name: item.route }"
        exact-active-class="active"
        class="menu-item-link"
      >
        <p class="menu-item">{{ item.label }}</p>
      </RouterLink>
      <p class="menu-item" v-if="'handler' in item" @click="item.handler">{{ item.label }}</p>
    </div>
  </div>
</template>

<style>
.menu-container {
  display: flex;
  gap: 6px;
  align-items: center;
}

.menu-item {
  padding: 4px 6px;
  border: 1px solid black;
  cursor: pointer;
}

.menu-item-link {
  text-decoration: none;
  color: inherit;
}

.active {
  font-weight: bold;
}
</style>