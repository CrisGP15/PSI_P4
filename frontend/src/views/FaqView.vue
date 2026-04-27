
<template>
  <div class="faq">
    <h1>Preguntas Frecuentes</h1>
    
    <div class="faq-item">
      <h3>¿Cómo funciona la aplicación?</h3>
      <p>Escuchas una canción y completas las palabras que faltan en la letra en tiempo real.</p>
    </div>
    
    <div class="faq-item">
      <h3>¿Necesito registrarme?</h3>
      <p>No es obligatorio, pero si te registras guardamos tu progreso y estadísticas.</p>
    </div>
    
    <div class="faq-item">
      <h3>¿Cómo se cuentan los fallos?</h3>
      <p>Cada intento fallido al escribir una palabra cuenta como un fallo. Si fallas dos veces la misma palabra, son dos fallos.</p>
    </div>
    
    <div class="faq-item">
      <h3>¿Qué pasa si no escribo nada?</h3>
      <p>La reproducción se parará automáticamente al final de la frase actual.</p>
    </div>
    
    <div class="faq-item">
      <h3>¿Puedo saltarme una palabra?</h3>
      <p>Sí, hay un botón "Skip" que te permite saltar la palabra actual, pero contará como un fallo.</p>
    </div>
  </div>
</template>

<script setup>

</script>

<style scoped>
.faq {
  color: #333;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.faq-item {
  background-color: #f5f5f5;
  margin: 20px 0;
  padding: 15px;
  border-radius: 8px;
}

.faq-item h3 {
  color: #42b983;
  margin-bottom: 10px;
}
</style>