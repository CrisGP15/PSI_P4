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
      

        <!-- Línea sin hueco: texto normal -->
        <template v-if="!line.word">
          <span>{{ line.text }}</span>
        </template>

        <!-- Línea con hueco -->
        <template v-else>
          <span>{{ line.before }}</span>

          <!-- Input real de Vue: solo activo en la línea actual -->
          <input
            v-if="line.isCurrent"
            v-model="userInput"
            type="text"
            class="word-input"
            :class="{
              correct: inputState === 'correct',
              wrong:   inputState === 'wrong'
            }"
            placeholder="___"
            @input="checkWord(line)"
            autocomplete="off"
            autocorrect="off"
            autocapitalize="off"
            spellcheck="false"
          />
          <!-- En líneas no activas mostrar el hueco como guiones -->
          <span v-else class="blank">___</span>

          <span>{{ line.after }}</span>
        </template>
      </div>
    </div>

    <!-- Botón skip: solo visible cuando la línea actual tiene un hueco -->
    <div v-if="currentLineHasWord" class="skip-wrap">
      <button class="btn-skip" @click="skip">Skip</button>
    </div>

   
    <div v-if="finished" class="summary">
      <h2>Canción completada</h2>
      <p>Respuestas correctas: <strong>{{ correctCount }}</strong></p>
      <p>Errores cometidos: <strong>{{ errorCount }}</strong></p>
      <p>Porcentaje de aciertos: <strong>{{ successRate }}%</strong></p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue'

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

// ── Estado 
const lyricsData       = ref([])
const currentLineIndex = ref(-1)
const visibleLines     = ref([])


const userInput    = ref('')
const inputState   = ref('')     
const correctCount = ref(0)
const errorCount   = ref(0)
const finished     = ref(false)

// ── Carga del archivo LRC 
onMounted(async () => {
  await loadLyrics()
})

async function loadLyrics() {
  try {
    const response = await fetch(props.lyricsUrl)
    const text     = await response.text()
    parseLRC(text)
  } catch (error) {
    console.error('Error loading lyrics:', error)
  }
}


function parseLRC(lrcText) {
  const lines  = lrcText.split('\n')
  const parsed = []

  lines.forEach(line => {
    const match = line.match(/\[(\d{2}):(\d{2})\.(\d{2})\](.*)/)
    if (!match) return

    const minutes = parseInt(match[1])
    const seconds = parseInt(match[2])
    const time    = minutes * 60 + seconds
    const text    = match[4].trim()

    if (!text) return

   
    const wordMatch = text.match(/\{(\w+)\}/)
    if (wordMatch) {
      const word   = wordMatch[1]
      const idx    = text.indexOf('{' + word + '}')
      const before = text.slice(0, idx)
      const after  = text.slice(idx + word.length + 2)
      parsed.push({ time, text, word, before, after, answered: false })
    } else {
      parsed.push({ time, text, word: null, before: '', after: '', answered: false })
    }
  })

  lyricsData.value = parsed
  if (parsed.length > 0) {
    currentLineIndex.value = 0
    updateVisibleLines()
  }
}

//  Sincronización con el tiempo del audio 
watch(() => props.currentTime, (time) => {
  updateCurrentLine(time)
})

function updateCurrentLine(time) {
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

   
    const line = lyricsData.value[newIndex]
    if (line && line.word && !line.answered) {
      userInput.value  = ''
      inputState.value = ''
      emit('stopAudio')
      nextTick(() => {
        const input = document.querySelector('.word-input')
        if (input) input.focus()
      })
    }
  }
}


function updateVisibleLines() {
  const lines = []
  for (let i = -1; i <= 1; i++) {
    const index = currentLineIndex.value + i
    if (index >= 0 && index < lyricsData.value.length) {
      lines.push({
        ...lyricsData.value[index],
        isCurrent: i === 0
      })
    }
  }
  visibleLines.value = lines
}

// ── Validación de la palabra 
function checkWord(line) {
  if (!line || !line.word) return

  const typed   = userInput.value.trim().toLowerCase()
  const correct = line.word.toLowerCase()

  if (typed === correct) {
    inputState.value = 'correct'
    lyricsData.value[currentLineIndex.value].answered = true
    correctCount.value++
    setTimeout(() => {
      userInput.value  = ''
      inputState.value = ''
      emit('startAudio')
    }, 300)
  } else if (typed.length >= correct.length) {
    inputState.value = 'wrong'
    errorCount.value++
    setTimeout(() => {
      userInput.value  = ''
      inputState.value = ''
    }, 400)
  }
}

//  Botón skip 
function skip() {
  const line = lyricsData.value[currentLineIndex.value]
  if (!line || !line.word) return
  errorCount.value++
  lyricsData.value[currentLineIndex.value].answered = true
  userInput.value  = ''
  inputState.value = ''
  emit('startAudio')
}

//  Fin de canción
function handleSongEnded() {
  finished.value = true
  emit('summary', {
    correct: correctCount.value,
    errors:  errorCount.value,
    total:   lyricsData.value.filter(l => l.word).length,
  })
}
defineExpose({ handleSongEnded })

//  Computed 
const currentLineHasWord = computed(() => {
  const line = lyricsData.value[currentLineIndex.value]
  return line && line.word && !line.answered
})

const successRate = computed(() => {
  const total = lyricsData.value.filter(l => l.word).length
  if (!total) return 0
  return Math.round((correctCount.value / total) * 100)
})
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
  background-color: #2e2e2b;
  font-weight: bold;
  border-left: 4px solid #42b983;
  border-radius: 0;
  padding-left: 10px;
}

.blank {
  display: inline-block;
  min-width: 3rem;
  border-bottom: 2px solid #ccc;
  margin: 0 4px;
  vertical-align: bottom;
}

.word-input {
  display: inline-block;
  width: 8rem;
  padding: 2px 8px;
  font-size: 1rem;
  font-family: monospace;
  border: 2px solid #ccc;
  border-radius: 4px;
  text-align: center;
  margin: 0 4px;
  vertical-align: middle;
  transition: border-color 0.15s, background 0.15s;
}
.word-input:focus {
  outline: none;
  border-color: #42b983;
}
.word-input.correct {
  border-color: #42b983;
  background: #e8f8f0;
  color: #27ae60;
}
.word-input.wrong {
  border-color: #e74c3c;
  background: #fdf0ed;
  color: #e74c3c;
}

.skip-wrap {
  margin-top: 8px;
}
.btn-skip {
  padding: 4px 16px;
  font-size: 0.875rem;
  background: transparent;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  color: #666;
}
.btn-skip:hover {
  background: #f5f5f5;
}

.summary {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #f0faf5;
  border: 1px solid #42b983;
  border-radius: 8px;
}
.summary h2 {
  font-size: 1.1rem;
  margin: 0 0 0.75rem;
  color: #1a1a1a;
}
.summary p {
  margin: 0.3rem 0;
  font-size: 0.95rem;
}
</style>