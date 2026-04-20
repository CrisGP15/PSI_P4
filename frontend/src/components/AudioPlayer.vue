<template>
  <div class="audio-player">
    <audio 
      ref="audio"
      :src="audioSrc"
      @timeupdate="emitTimeUpdate"
      @ended="emitEnded"
      controls
    ></audio>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
const audio = ref(null)

const props = defineProps({
  audioUrl: {
    type: String,
    required: true
  },
  stopAudio: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['timeUpdate', 'ended'])
const audioElement = ref(null)

function emitTimeUpdate() {
  emit('onTimeUpdate', event.target.currentTime)
}

function emitEnded() {
  emit('onEnded')
}

// Observar si se debe parar el audio
watch(() => props.stopAudio, (shouldStop) => {
  if (shouldStop && audioElement.value) {
    audioElement.value.pause()
  } else if (!shouldStop && audioElement.value) {
    audioElement.value.play()
  }
})
</script>