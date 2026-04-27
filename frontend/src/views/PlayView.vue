<template>
  <div class="play-view" :style="backgroundStyle">
    <div class="content-overlay">
      <div class="song-header" v-if="song">
        <h1>{{ song.title }}</h1>
        <p class="artist">{{ song.artist }}</p>
      </div>

      <div class="audio-section">
        <AudioPlayer
          v-show="song?.audio_url"
          ref="audioPlayerRef"
          :audio-src="song?.audio_url || ''"
          :stop-audio="stopAudioFlag"
          @on-time-update="handleTimeUpdate"
          @on-ended="handleSongEnded"
        />
      </div>

      <div class="lyrics-section" v-if="song?.lyrics_url">
        <LyricsDisplay
          ref="lyricsDisplayRef"
          :lyrics-url="song.lyrics_url"
          :current-time="currentTime"
          @stop-audio="handleStopAudio"
          @start-audio="handleStartAudio"
          @summary="handleSummary"
          @word-completed="handleWordCompleted"
        />
      </div>

      <div v-if="loading" class="loading">
        <p>Cargando canción...</p>
      </div>

      <div v-if="error" class="error">
        <p>{{ error }}</p>
        <button @click="retryLoad">Reintentar</button>
      </div>

      <div v-if="showSummary" class="summary-modal">
        <div class="summary-content">
          <h2>¡Canción Completada!</h2>
          <p>Aciertos: {{ summary.correct }}</p>
          <p>Fallos: {{ summary.wrong }}</p>
          <p>Porcentaje: {{ percentage }}%</p>
          <button @click="goHome">Volver al Inicio</button>
          <button @click="playAgain">Repetir Canción</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import AudioPlayer from "../components/AudioPlayer.vue";
import LyricsDisplay from "../components/LyricsDisplay.vue";

// Router y Store
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

// Referencias a componentes
const audioPlayerRef = ref(null);
const lyricsDisplayRef = ref(null);

// Estado reactivo
const loading = ref(true);
const error = ref(null);
const song = ref(null);
const currentTime = ref(0);
const stopAudioFlag = ref(false);
const showSummary = ref(false);
const summary = ref({ correct: 0, wrong: 0 });
const songUserSent = ref(false);

// URL de la API
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8001"; //-----si da error, a ver si añadir una / al final se soluciona

// Estilo de fondo (si hay imagen)
const backgroundStyle = computed(() => {
  if (song.value?.background_image) {
    return {
      backgroundImage: `url(${song.value.background_image})`,
      backgroundSize: "cover",
      backgroundPosition: "center",
    };
  }
  return {};
});

// Calcular porcentaje
const percentage = computed(() => {
  const total = summary.value.correct + summary.value.wrong;
  if (total === 0) return 0;
  return Math.round((summary.value.correct / total) * 100);
});

// Cargar datos de la canción al montar el componente
onMounted(() => {
  loadSong();
});

// Limpiar al desmontar
onUnmounted(() => {
  // Evitar enviar datos duplicados
  songUserSent.value = true;
});

// Obtener el ID de la canción de la URL
function getSongId() {
  // Soporta tanto /play/:id como /songs/:id
  return route.params.id || route.query.id;
}

// Cargar canción desde la API
async function loadSong() {
  loading.value = true;
  error.value = null;
  showSummary.value = false;
  songUserSent.value = false;

  const songId = getSongId();

  if (!songId) {
    // Si no hay ID, cargar una canción aleatoria
    await loadRandomSong();
    return;
  }

  try {
    const response = await fetch(`${API_URL}/api/v1/songs/${songId}/`);

    if (!response.ok) {
      throw new Error(`Error ${response.status}: No se pudo cargar la canción`);
    }

    const data = await response.json();

    const baseURL = API_URL; //http://localhost:8001
    song.value = {
      ...data,
      audio_url: data.audio_file,
      lyrics_url: data.lrc_file,
      background_image: data.background_image,
    };
  } catch (err) {
    console.error("Error cargando canción:", err);
    error.value = err.message;

    // Datos de ejemplo para pruebas locales
    song.value = {
      id: songId,
      title: "Here in the real world",
      artist: "Alan Jackson",
      audio_url: `${API_URL}/media/media/Alan_Jackson_-_Here_In_The_Real_World.mp3`,
      lyrics_url: `${API_URL}/media/media/Alan_Jackson_-_Here_In_The_Real_World.lrc`,
      background_image: null,
    };
  } finally {
    loading.value = false;
  }
}

// Cargar canción aleatoria
async function loadRandomSong() {
  try {
    const response = await fetch(`${API_URL}/api/v1/songs/random/`);

    if (!response.ok) {
      throw new Error("No se pudo cargar canción aleatoria");
    }

    const data = await response.json();
    const baseURL = API_URL; //http://localhost:8001
    song.value = {
      ...data,
      audio_url: data.audio_file,
      lyrics_url: data.lrc_file,
      background_image: data.background_image,
    };
  } catch (err) {
    console.error("Error cargando canción aleatoria:", err);

    // Datos de ejemplo
    song.value = {
      id: songId,
      title: "Here in the real world",
      artist: "Alan Jackson",
      audio_url: `${API_URL}/media/media/Alan_Jackson_-_Here_In_The_Real_World.mp3`,
      lyrics_url: `${API_URL}/media/media/Alan_Jackson_-_Here_In_The_Real_World.lrc`,
      background_image: null,
    };
  } finally {
    loading.value = false;
  }
}

// Manejar actualización de tiempo desde AudioPlayer
function handleTimeUpdate(time) {
  currentTime.value = time;
}

// Manejar fin de la canción
async function handleSongEnded() {
  // Esperar un momento para que LyricsDisplay procese el resumen
  setTimeout(() => {
    if (!showSummary.value) {
      // Si no hay resumen, forzar mostrar
      showSummaryModal();
    }
  }, 500);
}

// Manejar parada de audio solicitada por LyricsDisplay
function handleStopAudio() {
  stopAudioFlag.value = true;
}

// Manejar inicio de audio solicitado por LyricsDisplay
function handleStartAudio() {
  stopAudioFlag.value = false;
}

// Manejar resumen de palabras desde LyricsDisplay
async function handleSummary(summaryData) {
  console.log("Resumen recibido:", summaryData);
  summary.value = summaryData;
  showSummary.value = true;

  // Si el usuario está autenticado, guardar en SongUser
  if (authStore.isAuthenticated && !songUserSent.value && song.value) {
    await saveSongUserResults();
  }
}

// Manejar palabra completada (para estadísticas)
function handleWordCompleted(wordData) {
  // Opcional: actualizar progreso en tiempo real
  console.log("Palabra completada:", wordData);
}

// Guardar resultados en SongUser
async function saveSongUserResults() {
  if (songUserSent.value) return;

  try {
    const response = await fetch(`${API_URL}/api/v1/songusers/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // 'Authorization': `Bearer ${authStore.token}`
        Authorization: `Token ${authStore.token}`,
      },
      body: JSON.stringify({
        song: song.value.id,
        correct_guesses: summary.value.correct,
        wrong_guesses: summary.value.wrong,
      }),
    });

    if (response.ok) {
      console.log("Resultados guardados en SongUser");
      songUserSent.value = true;
    } else {
      console.error("Error guardando resultados:", await response.text());
    }
  } catch (err) {
    console.error("Error en petición SongUser:", err);
  }
}

// Mostrar modal de resumen
function showSummaryModal() {
  // Obtener resumen de LyricsDisplay si no se ha recibido
  if (lyricsDisplayRef.value) {
    const finalSummary = lyricsDisplayRef.value.getSummary();
    summary.value = finalSummary;
  }
  showSummary.value = true;

  // Guardar resultados si es necesario
  if (authStore.isAuthenticated && !songUserSent.value && song.value) {
    saveSongUserResults();
  }
}

// Reintentar carga
function retryLoad() {
  loadSong();
}

// Volver al inicio
function goHome() {
  router.push("/");
}

// Repetir la misma canción
function playAgain() {
  showSummary.value = false;
  summary.value = { correct: 0, wrong: 0 };
  currentTime.value = 0;
  stopAudioFlag.value = false;
  songUserSent.value = false;

  // Reiniciar componentes
  if (audioPlayerRef.value) {
    audioPlayerRef.value.reset();
  }
  if (lyricsDisplayRef.value) {
    lyricsDisplayRef.value.reset();
  }
}
</script>

<style scoped>
/* Contenedor principal */
.play-view {
  min-height: 100vh;
  width: 100%;
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}

/* Overlay para mejorar legibilidad */
.content-overlay {
  background: var(--color-background-overlay);
  min-height: 100vh;
  padding: var(--spacing-xl) var(--spacing-lg);
  backdrop-filter: blur(2px);
}

/* Cabecera de la canción */
.song-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.song-header h1 {
  font-size: var(--font-size-2xl);
  color: var(--color-text-light);
  margin-bottom: var(--spacing-xs);
}

.song-header .artist {
  font-size: var(--font-size-lg);
  color: var(--color-primary);
}

/* Reproductor de audio */
.audio-section {
  max-width: 600px;
  width: 100%;
  margin: 0 auto var(--spacing-xl);
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md);
}

/* Sección de letra */
.lyrics-section {
  max-width: 900px;
  width: 90%;
  margin: 0 auto;
  background: rgba(0, 0, 0, 0.6);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  min-height: 400px;
}

/* Estados de carga/error */
.loading,
.error {
  text-align: center;
  padding: var(--spacing-xl);
}

.loading {
  color: var(--color-text-muted);
}

.error {
  color: var(--color-error);
}

.error button {
  margin-top: var(--spacing-sm);
  padding: var(--spacing-xs) var(--spacing-sm);
  background-color: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  transition: background var(--transition-fast);
}

.error button:hover {
  background-color: var(--color-primary-dark);
}

/* Modal de resumen */
.summary-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.95);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn var(--transition-normal);
}

.summary-content {
  background: var(--color-text-light);
  color: var(--color-background-dark);
  padding: var(--spacing-xl);
  border-radius: var(--border-radius-lg);
  text-align: center;
  max-width: 400px;
  width: 90%;
  animation: slideUp var(--transition-normal);
}

.summary-content h2 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-md);
}

.summary-content p {
  font-size: var(--font-size-md);
  margin: var(--spacing-sm) 0;
}

.summary-content button {
  margin: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-lg);
  background-color: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.summary-content button:hover {
  background-color: var(--color-primary-dark);
  transform: translateY(-2px);
}

/* Animaciones */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .content-overlay {
    padding: var(--spacing-md);
  }

  .song-header h1 {
    font-size: var(--font-size-lg);
  }

  .song-header .artist {
    font-size: var(--font-size-md);
  }

  .lyrics-section {
    width: 95%;
    padding: var(--spacing-md);
  }

  .summary-content {
    padding: var(--spacing-lg);
    width: 95%;
  }
}
</style>
