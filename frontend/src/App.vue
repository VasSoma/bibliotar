<template>
  <div id="app">
    <HeaderComponent />
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup>
import HeaderComponent from './components/Header.component.vue';
</script>