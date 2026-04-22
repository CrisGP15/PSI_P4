import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const isAuthenticated = ref(!!token.value)

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

  async function login(username, password) {
    try {
      const response = await fetch(`${API_URL}/api/v1/token/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.non_field_errors?.[0] || 'Login failed')
      }
      
      const data = await response.json()
      token.value = data.auth_token
      localStorage.setItem('token', data.auth_token)
      isAuthenticated.value = true
      return true
    } catch (err) {
      console.error('Login error:', err)
      return false
    }
  }

  async function logout() {
    if (token.value) {
      try {
        await fetch(`${API_URL}/api/v1/token/logout/`, {
          method: 'POST',
          headers: {
            'Authorization': `Token ${token.value}`,
            'Content-Type': 'application/json'
          }
        })
      } catch (err) {
        console.error('Logout error:', err)
      }
    }
    token.value = null
    localStorage.removeItem('token')
    isAuthenticated.value = false
  }

  return { token, isAuthenticated, login, logout }
})