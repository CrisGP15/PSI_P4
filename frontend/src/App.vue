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

/* Header */
.app-header {
  background-color: var(--color-background-dark-header);
  border-bottom: 1px solid rgba(0, 96, 27, 0.687);
  padding: var(--spacing-md) var(--spacing-lg);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: var(--content-max-width);
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.app-header h1 {
  font-size: var(--font-size-lg);
  margin: 0;
  background: linear-gradient(135deg, var(--color-primary), #62b69b);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}

/* Navegación */
.navbar {
  display: flex;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.navbar a {
  color: var(--color-text-light);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  transition: all var(--transition-fast);
}

.navbar a:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.navbar a.router-link-active {
  background-color: var(--color-primary);
  color: white;
}

/* Contenido principal */
.app-content {
  flex: 1;
  width: 100%;
  margin: 0 auto;
}

/* Responsive */
@media (max-width: 768px) {
  .app-header {
    padding: var(--spacing-sm);
  }
  
  .header-content {
    flex-direction: column;
    text-align: center;
  }
  
  .app-header h1 {
    font-size: var(--font-size-md);
  }
}
</style>
