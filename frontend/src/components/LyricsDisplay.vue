<template>
  <div class="lyrics-display">
    <div class="lyrics-container">
      <div
        v-for="(line, index) in visibleLines"
        :key="index"
        :class="{ 'current-line': line.isCurrent }"
        class="lyric-line"
      >
        <template v-if="!line.word">
          <span>{{ line.text }}</span>
        </template>

        <template v-else>
          <span>{{ line.before }}</span>

          <!-- Palabra ya respondida: se muestra como texto -->
          <span v-if="line.answered" class="answered-word">
            {{ line.word }}
          </span>
    
          <!-- Input activo solo si es la línea actual y no respondida -->
          <input
            v-else-if="line.isCurrent"
            v-model="userInput"
            data-cy="blankInput"
            type="text"
            class="word-input"
            :class="{ wrong: inputState === 'wrong' }"
            placeholder="___"
            @keyup.enter="checkWord(currentLineIndex)"
            autocomplete="off"
            autocorrect="off"
            autocapitalize="off"
            spellcheck="false"
          />

          <!-- Línea inactiva y no respondida: hueco -->
          <span v-else class="blank">___</span>

          <span>{{ line.after }}</span>
        </template>
      </div>
    </div>


    <div v-if="currentLineHasWord" class="skip-wrap">
      <button class="btn-skip" data-cy="skip" @click="skip(currentLineIndex)">Skip</button>
    </div>

    <div v-if="finished" class="summary">
      <h2>Canción completada</h2>
      <p>Correctas: <strong>{{ correctCount }}</strong></p>
      <p>Fallos: <strong>{{ errorCount }}</strong></p>
      <p>Porcentaje: <strong>{{ successRate }}%</strong></p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'

const props = defineProps({
  lyricsUrl: { type: String, required: true },
  currentTime: { type: Number, default: 0 }
})

const emit = defineEmits(["stopAudio", "startAudio", "summary"]);

// Estado
const lyricsData = ref([])
const currentLineIndex = ref(-1)
const visibleLines = ref([])
const userInput = ref('')
const inputState = ref('')
const correctCount = ref(0)
const errorCount = ref(0)
const finished = ref(false)

onMounted(async () => {
  await loadLyrics()
  if (lyricsData.value.length) {
    updateCurrentLine(props.currentTime)  // inicializar índice según tiempo actual
  }
})

async function loadLyrics() {
  try {
    const res = await fetch(props.lyricsUrl)
    const text = await res.text()
    parseLRC(text)
  } catch (err) {
    console.error('Error cargando letras:', err)
  }
}

function parseLRC(lrcText) {
  const lines = lrcText.split('\n')
  const parsed = []

  lines.forEach(line => {
    const match = line.match(/\[(\d{2}):(\d{2})\.(\d{2})\](.*)/)
    if (!match) return
    const minutes = parseInt(match[1])
    const seconds = parseInt(match[2])
    const time = minutes * 60 + seconds
    const text = match[4].trim()
    if (!text) return

    const wordMatch = text.match(/\{(\w+)\}/)
    if (wordMatch) {
      const word = wordMatch[1]
      const idx = text.indexOf('{' + word + '}')
      const before = text.slice(0, idx)
      const after = text.slice(idx + word.length + 2)
      parsed.push({ time, text, word, before, after, answered: false })
    } else {
      parsed.push({
        time,
        text,
        word: null,
        before: "",
        after: "",
        answered: false,
      });
    }
  });

  lyricsData.value = parsed
  if (parsed.length) {
    currentLineIndex.value = 0
    updateVisibleLines()
  }
}

watch(() => props.currentTime, (time) => {
  updateCurrentLine(time)
})

function updateCurrentLine(time) {   
  // Si la línea actual tiene palabra NO respondida, no cambiar de línea
  if (currentLineIndex.value >= 0) {
    const curr = lyricsData.value[currentLineIndex.value]
    if (curr && curr.word && !curr.answered) {
      // Calcular final de esta línea (tiempo de la siguiente)
      let nextTime = Infinity
      if (currentLineIndex.value + 1 < lyricsData.value.length) {
        nextTime = lyricsData.value[currentLineIndex.value + 1].time
      }
      // Si hemos superado el final de la línea y aún no respondió → pausar
      if (time >= nextTime - 0.05) {
        emit('stopAudio')
      }
      return // No avanzar
    }
  }

  // Calcular nueva línea según el tiempo
  let newIndex = -1
  for (let i = 0; i < lyricsData.value.length; i++) {
    if (time >= lyricsData.value[i].time) {
      newIndex = i;
    } else {
      break;
    }
  }

  // Si el tiempo es anterior a la primera línea, mostrar la primera como "próxima"
  if (newIndex === -1 && lyricsData.value.length) {
    newIndex = 0
  }

  if (newIndex !== currentLineIndex.value) {
    currentLineIndex.value = newIndex
    updateVisibleLines()
  }
}

function updateVisibleLines() {
  const lines = [];
  for (let i = -1; i <= 1; i++) {
    const idx = currentLineIndex.value + i
    if (idx >= 0 && idx < lyricsData.value.length) {
      lines.push({
        ...lyricsData.value[idx],
        isCurrent: i === 0
      })
    }
  }
  visibleLines.value = lines;
}

function checkWord(lineIndex) {
  const line = lyricsData.value[lineIndex]
  if (!line || !line.word || line.answered) return

  const typed = userInput.value.trim().toLowerCase()
  const correctWord = line.word.toLowerCase()

  if (typed === correctWord) {
    // Acierto
    line.answered = true

    correctCount.value++
    userInput.value = ''
    inputState.value = ''


    lyricsData.value = [...lyricsData.value]

    
    emit('startAudio')
    // updateCurrentLine(props.currentTime) // actualizar índice 
     // Forzar recálculo de la línea actual con un pequeño offset
    setTimeout(() => {
      // Buscar la siguiente línea que tenga palabra y no esté respondida
      let nextIndex = -1
      for (let i = currentLineIndex.value + 1; i < lyricsData.value.length; i++) {
        if (lyricsData.value[i].word && !lyricsData.value[i].answered) {
          nextIndex = i
          break
        }
      }
      
      if (nextIndex !== -1) {
        currentLineIndex.value = nextIndex
        updateVisibleLines()
      } else {
        // Si no hay más palabras, avanzar al final
        currentLineIndex.value = lyricsData.value.length - 1
        updateVisibleLines()
      }
    }, 50)
  } else {
    // Error
    inputState.value = 'wrong'
    errorCount.value++
    userInput.value = ''
    setTimeout(() => {
      inputState.value = ''
    }, 400)
    // No emitimos startAudio, la música sigue pausada si lo estaba
  }
}

function skip(lineIndex) {
  const line = lyricsData.value[lineIndex]
  if (!line || !line.word || line.answered) return

  line.answered = true
  errorCount.value++
  userInput.value = ''
  inputState.value = ''

  // Forzar actualización reactiva
  lyricsData.value = [...lyricsData.value]

  emit('startAudio')
  setTimeout(() => {
    // Buscar la siguiente línea con palabra pendiente
    let nextIndex = -1
    for (let i = currentLineIndex.value + 1; i < lyricsData.value.length; i++) {
      if (lyricsData.value[i].word && !lyricsData.value[i].answered) {
        nextIndex = i
        break
      }
    }
    
    if (nextIndex !== -1) {
      currentLineIndex.value = nextIndex
      updateVisibleLines()
    }
  }, 50)
}

function handleSongEnded() {
  finished.value = true;
  emit("summary", {
    correct: correctCount.value,
    errors: errorCount.value,
    total: lyricsData.value.filter(l => l.word).length
  })
}

const currentLineHasWord = computed(() => {
  const line = lyricsData.value[currentLineIndex.value];
  return line && line.word && !line.answered;
});

const successRate = computed(() => {
  const total = lyricsData.value.filter(l => l.word).length
  if (!total) return 0
  return Math.round((correctCount.value / total) * 100)
})

defineExpose({ handleSongEnded, getSummary: () => ({ correct: correctCount.value, wrong: errorCount.value }) })
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
  background: #ff0000;
}

.summary {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #41725a;
  border: 1px solid #42b983;
  border-radius: 8px;
}

.summary h2 {
  font-size: 1.1rem;
  margin: 0 0 0.75rem;
}

.summary p {
  margin: 0.3rem 0;
  font-size: 0.95rem;
}

</style>
