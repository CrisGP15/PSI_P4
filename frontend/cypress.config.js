// cypress.config.js - Versión CommonJS (la que funciona siempre)
const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    specPattern: 'cypress/e2e/**/*.{cy,spec}.{js,jsx,ts,tsx}',
    baseUrl: 'http://localhost:5173',  // ← CAMBIA A LOCAL
    supportFile: 'cypress/support/e2e.js',
  },
  component: {
    specPattern: 'src/**/__tests__/*.{cy,spec}.{js,ts,jsx,tsx}',
    supportFile: 'cypress/support/component.js',
    devServer: {
      framework: 'vue',
      bundler: 'vite',
    },
  },
})