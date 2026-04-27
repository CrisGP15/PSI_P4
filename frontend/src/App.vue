<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <div id="app">
    <header class="app-header">
      <div class="header-content">
        <h1>🎵 SongProject</h1>
        <nav class="navbar">
          <RouterLink to="/">Home</RouterLink>
          <RouterLink to="/faq">FAQ</RouterLink>
          <RouterLink v-if="!authStore.isAuthenticated" to="/log-in">Login</RouterLink>
          <RouterLink v-if="authStore.isAuthenticated" to="/log-out">Logout</RouterLink>
        </nav>
      </div>
    </header>

    <main class="app-content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background-color: #2c3e50;
  color: white;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
}

.app-header h1 {
  margin: 0 0 1rem 0;
  font-size: 2rem;
}

.navbar {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.navbar a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.navbar a:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.navbar a.router-link-active {
  background-color: #42b983;
}

.app-content {
  flex: 1;
  max-width: none !important;
  width: 100% !important;
  margin: 0 auto;
  padding: 2rem;
}

@media (max-width: 768px) {
  .app-header h1 {
    font-size: 1.5rem;
  }

  .navbar {
    gap: 0.5rem;
  }

  .navbar a {
    padding: 0.5rem 0.75rem;
    font-size: 0.9rem;
  }
}
</style>
