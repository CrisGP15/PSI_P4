<template>
  <div class="lyrics-display">
    <div class="lyrics-container">
      <!-- Mostrar líneas de la letra -->
      <div 
        v-for="(line, index) in visibleLines" 
        :key="index"
        :class="{ 'current-line': line.isCurrent }"
        class="lyric-line"
      >
        <!-- Precesar cada línea reemplazando {palabra} con inputs -->
        <span v-html="processLine(line.text)"></span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  lyricsUrl: {
    type: String,
    required: true
  },
  currentTime: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['stopAudio', 'startAudio', 'summary'])

const lyricsData = ref([]) // Array de objetos {time, text}
const currentLineIndex = ref(-1)
const visibleLines = ref([])

// Cargar archivo LRC
onMounted(async () => {
  await loadLyrics()
})

async function loadLyrics() {
  try {
    const response = await fetch(props.lyricsUrl)
    const text = await response.text()
    parseLRC(text)
  } catch (error) {
    console.error('Error loading lyrics:', error)
  }
}

function parseLRC(lrcText) {
  
  const lines = lrcText.split('\n')
  const parsed = []
  
  lines.forEach(line => {
    const match = line.match(/\[(\d{2}):(\d{2})\.(\d{2})\](.*)/)
    if (match) {
      const minutes = parseInt(match[1])
      const seconds = parseInt(match[2])
      const time = minutes * 60 + seconds
      const text = match[4].trim()
      if (text) {
        parsed.push({ time, text })
      }
    }
  })
  
  lyricsData.value = parsed
}

// Observar cambios en currentTime para actualizar la línea actual
watch(() => props.currentTime, (time) => {
  updateCurrentLine(time)
})

function updateCurrentLine(time) {
  // Encontrar la línea actual basada en el tiempo
  let newIndex = -1
  for (let i = 0; i < lyricsData.value.length; i++) {
    if (time >= lyricsData.value[i].time) {
      newIndex = i
    } else {
      break
    }
  }
  
  if (newIndex !== currentLineIndex.value) {
    currentLineIndex.value = newIndex
    updateVisibleLines()
  }
}

function updateVisibleLines() {
  // Mostrar línea actual, anterior y siguiente
  const lines = []
  for (let i = -1; i <= 1; i++) {
    const index = currentLineIndex.value + i
    if (index >= 0 && index < lyricsData.value.length) {
      lines.push({
        text: lyricsData.value[index].text,
        isCurrent: i === 0
      })
    }
  }
  visibleLines.value = lines
}

function processLine(lineText) {
  // Reemplazar {palabra} con inputs
  // Esto es complejo y lo harás después
  return lineText.replace(/\{([^}]+)\}/g, '<input type="text" placeholder="___" />')
}
</script>

<style scoped>
.lyrics-container {
  font-family: monospace;
  font-size: 16px;
  line-height: 1.8;
}
.lyric-line {
  margin: 10px 0;
  padding: 5px;
}
.current-line {
  background-color: #ffff99;
  font-weight: bold;
  border-left: 4px solid #42b983;
  padding-left: 10px;
}
</style>