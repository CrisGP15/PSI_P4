Cypress.on('uncaught:exception', (err) => {
  if (
    err.message.includes('no supported sources') ||
    err.message.includes('NotSupportedError') ||
    err.name === 'NotSupportedError'
  ) {
    return false
  }
})