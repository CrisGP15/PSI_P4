<template>
  <div class="play-view">
    <h2>Reproduciendo Canción</h2>
    
    <!-- Aquí irá el AudioPlayer -->
    <div class="audio-section">
      <AudioPlayer 
        v-if="songData.audio_url"
        :audio-url="songData.audio_url"
        @time-update="handleTimeUpdate"
        @ended="handleSongEnded"
      />
    </div>
    
    <!-- Aquí irá el LyricsDisplay -->
    <div class="lyrics-section">
      <LyricsDisplay 
        v-if="songData.lyrics_url"
        :lyrics-url="songData.lyrics_url"
        :current-time="currentTime"
        @stop-audio="stopAudio"
        @start-audio="startAudio"
        @summary="handleSummary"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AudioPlayer from '../components/AudioPlayer.vue'
import LyricsDisplay from '../components/LyricsDisplay.vue'

const route = useRoute()
const songData = ref({})
const currentTime = ref(0)
const audioPlaying = ref(true)

// Cargar datos de la canción cuando se monta el componente
onMounted(async () => {
  const songId = route.params.id || 1 // Si no hay ID, carga la primera
  await loadSong(songId)
})

async function loadSong(id) {
  // Aquí harás fetch a tu API de Django
  // Por ahora, datos de ejemplo
  songData.value = {
    id: id,
    title: 'Example Song',
    audio_url: 'URL_DEL_AUDIO',
    lyrics_url: 'URL_DEL_ARCHIVO_LRC'
  }
}

function handleTimeUpdate(time) {
  currentTime.value = time
}

function handleSongEnded() {
  console.log('Canción terminada')
}

function stopAudio() {
  audioPlaying.value = false
}

function startAudio() {
  audioPlaying.value = true
}

async function handleSummary(summary) {
  console.log('Resumen:', summary)
  // Aquí enviarás los resultados a la API si el usuario está autenticado
}
</script>

<style scoped>
.play-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
.audio-section {
  margin-bottom: 30px;
}
.lyrics-section {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
}
</style>