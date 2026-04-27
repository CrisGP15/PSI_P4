<template>
  <main class="home">

    <!-- Descripción de la aplicación -->
    <section class="hero">
      <h1>SongProject</h1>
      <h2>Learn a language through songs</h2>
      <p class="description">
        "Songs" is the new way to learn English and other languages through music and the lyrics of your favourite songs. Improve and practise your listening skills with the best music videos. Fill in the gaps to the lyrics as you listen and sing Karaoke to your favourites
      </p>
    </section>

    <!-- Botón canción aleatoria -->
    <section class="random-section">
      <button
        class="btn-random"
        @click="goToRandomSong"
        :disabled="loadingRandom"
      >
        {{ loadingRandom ? 'Cargando...' : 'Random song' }}
      </button>
      <p v-if="randomError" class="error">{{ randomError }}</p>
    </section>

    <!-- Buscador -->
    <section class="search-section">
      <h2>Buscar canción</h2>
      <form @submit.prevent="searchSongs">
        <div class="search-bar">
          <input
            v-model="searchQuery"
            data-cy="search_text"
            type="text"
            placeholder="Escribe el título de una canción..."
            aria-label="Buscar canciones"
          />
          <button type="submit" :disabled="loadingSearch" data-cy="search_button">
            {{ loadingSearch ? 'Buscando...' : 'Buscar' }}
          </button>
        </div>
      </form>

      <!-- Resultados de búsqueda -->
      <div v-if="searchResults.length > 0" class="song-list">
        <h3>Resultados</h3>
        <ul>
          <li v-for="song in searchResults" :key="song.id">
            <RouterLink :to="`/songs/${song.id}`" :data-cy="song.title">
              {{ song.title }} — {{ song.artist }}
            </RouterLink>
          </li>
        </ul>
      </div>
      <p v-else-if="searchDone && !loadingSearch" class="no-results">
        No se encontraron canciones para "{{ searchQuery }}"
      </p>
      <p v-if="searchError" class="error">{{ searchError }}</p>
    </section>

    <!-- Top 3 canciones más populares -->
    <section class="top-songs">
      <h2>Canciones más populares</h2>

      <div v-if="loadingTop" class="loading">Cargando canciones...</div>
      <p v-else-if="topError" class="error">{{ topError }}</p>

      <ul v-else-if="topSongs.length > 0" >
        <li v-for="(song, index) in topSongs" :key="song.id" class="top-song-item">
          <span class="rank">{{ index + 1 }}</span>
          <RouterLink :to="`/songs/${song.id}`">
            <span class="song-title">{{ song.title }}</span>
            <span class="song-artist">{{ song.artist }}</span>
          </RouterLink>
          <span class="plays">{{ song.number_times_played }} plays</span>
        </li>
      </ul>

      <p v-else class="no-results">No hay canciones disponibles.</p>
    </section>

  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// URL base de la API — se define en el archivo .env
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

// ── Estado: Top 3 canciones 
const topSongs = ref([])
const loadingTop  = ref(false)
const topError    = ref(null)

async function fetchTopSongs() {
  loadingTop.value = true
  topError.value   = null
  try {
    const res = await fetch(
      `${API_URL}/api/v1/songs/top/?n=3`
    )
    if (!res.ok) throw new Error(`Error ${res.status}`)
    const data = await res.json()
    // El endpoint /top/ devuelve directamente un array
    topSongs.value = Array.isArray(data) ? data : (data.results ?? data)
  } catch (err) {
    topError.value = 'No se pudieron cargar las canciones populares.'
    console.error(err)
  } finally {
    loadingTop.value = false
  }
}

// ── Estado: Buscador 
const searchQuery = ref('')
const searchResults = ref([])
const loadingSearch = ref(false)
const searchError   = ref(null)
const searchDone    = ref(false)

async function searchSongs() {
  if (!searchQuery.value.trim()) return

  loadingSearch.value = true
  searchError.value   = null
  searchDone.value    = false
  searchResults.value = []

  try {
    const res = await fetch(
      `${API_URL}/api/v1/songs/search/?title=${encodeURIComponent(searchQuery.value)}`
    )
    if (!res.ok) throw new Error(`Error ${res.status}`)
    const data = await res.json()
    searchResults.value = Array.isArray(data) ? data : (data.results ?? data)
    searchDone.value    = true
  } catch (err) {
    searchError.value = 'Error al buscar canciones. Inténtalo de nuevo.'
    console.error(err)
  } finally {
    loadingSearch.value = false
  }
}

// ── Estado: Canción aleatoria 
const loadingRandom = ref(false)
const randomError   = ref(null)

async function goToRandomSong() {
  loadingRandom.value = true
  randomError.value   = null
  try {
    const res = await fetch(`${API_URL}/api/v1/songs/random/`)
    if (!res.ok) throw new Error(`Error ${res.status}`)
    const song = await res.json()
    router.push(`/songs/${song.id}`)
  } catch (err) {
    randomError.value = 'No se pudo obtener una canción aleatoria.'
    console.error(err)
  } finally {
    loadingRandom.value = false
  }
}

// ── Carga inicial 
onMounted(() => {
  fetchTopSongs()
})
</script>

<style scoped>
.home {
  max-width: none !important;
  width: 100% !important;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

/* Hero */
.hero h1 {
  color: #333;
  font-size: 2rem;
  margin: 0 0 0.5rem;
}
.hero p {
  color: #555;
  margin: 0;
}

.hero {
  text-align: center;
  margin-bottom: 1rem;
}

.hero h2 {
  font-size: 2.5rem;
  margin: 0 0 1rem 0;
  color: #42b983;
}

.hero .description {
  color: #555;
  line-height: 1.6;
  font-size: 1rem;
  max-width: none;
  margin: 0 auto;
}



/* Botón random */
.random-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
}
.btn-random {
  padding: 0.6rem 1.4rem;
  font-size: 1rem;
  background: #1a1a1a;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-random:hover:not(:disabled) {
  background: #333;
}
.btn-random:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Buscador */
.search-section h2,
.top-songs h2 {
  font-size: 1.2rem;
  margin: 0 0 1rem;
}
.search-bar {
  display: flex;
  gap: 0.5rem;
  max-width: 1200px;
  margin: 0 auto;
}
.search-bar input {
  flex: 1;
  padding: 0.5rem 0.75rem;
  font-size: 0.95rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}
.search-bar input:focus {
  outline: none;
  border-color: #1a1a1a;
}
.search-bar button {
  padding: 0.5rem 1rem;
  background: #1a1a1a;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.search-bar button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Listas de canciones */
.song-list h3 {
  font-size: 1rem;
  margin: 1rem 0 0.5rem;
  color: #444;
}
.song-list ul,
.top-songs ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.song-list li a,
.top-songs a {
  color: #1a1a1a;
  text-decoration: none;
  font-weight: 500;
}
.song-list li a:hover,
.top-songs a:hover {
  text-decoration: underline;
}

/* Top songs */
.top-song-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.6rem 0.75rem;
  border: 1px solid #eee;
  border-radius: 8px;
}
.rank {
  font-size: 1.1rem;
  font-weight: 700;
  color: #bbb;
  min-width: 1.5rem;
  text-align: center;
}
.top-song-item a {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}
.song-title {
  font-weight: 500;
  font-size: 0.95rem;
}
.song-artist {
  font-size: 0.8rem;
  color: #777;
}
.plays {
  font-size: 0.8rem;
  color: #999;
  white-space: nowrap;
}

/* Mensajes */
.loading   { color: #888; font-size: 0.9rem; }
.no-results { color: #888; font-size: 0.9rem; }
.error     { color: #c0392b; font-size: 0.9rem; }
</style>