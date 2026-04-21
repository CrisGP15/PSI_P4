<template>
  <div class="logout">
    
    <h1>Log Out</h1>
    <p>You will be redirected to the home page in 5 seconds.</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

onMounted(() => {
  // Hacer logout
  authStore.logout()
  
  // Redirigir después de 5 segundos
  setTimeout(() => {
    router.push('/')
  }, 5000)
})
</script>

<style scoped>
.logout {
  text-align: center;
  margin-top: 100px;
}
</style>