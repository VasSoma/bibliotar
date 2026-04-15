<script setup>
import axios from 'axios'

const login = async () => {
  const response = await axios.post('/loginurl')
  console.log(response.data)
}
</script>

<template>
  <div>
    <form @submit.prevent>
      <input />
      <input />
      <button @click="login">Login</button>
    </form>
  </div>
</template>

<style scoped></style>
