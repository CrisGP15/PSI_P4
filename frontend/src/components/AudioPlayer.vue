<template>
  <div class="audio-player">
    <audio
      id="my-audio"
      ref="audio"
      :src="audioSrc"
      @timeupdate="emitTimeUpdate"
      @ended="emitEnded"
      @error="handleAudioError"
      controls
    ></audio>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  audioSrc: {
    type: String,
    required: true
  },
  stopAudio: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['onTimeUpdate', 'onEnded'])


const audio = ref(null)


function emitTimeUpdate() {
   if (audio.value) emit('onTimeUpdate', audio.value.currentTime)
}

function emitEnded() {
  emit('onEnded')
}

function handleAudioError() {
  // Ignorar errores de src vacío mientras carga la canción
}


watch(() => props.stopAudio, (shouldStop) => {
  if (!audio.value || !props.audioSrc) return
  if (shouldStop) {
    audio.value.pause()
  } else {
    //audio.value.play()
    audio.value.play().catch(() => {})
  }
})
</script>