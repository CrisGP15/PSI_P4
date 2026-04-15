<template>
  <div class="audio-player">
    <audio 
      ref="audioElement"
      :src="audioUrl"
      @timeupdate="onTimeUpdate"
      @ended="onEnded"
      controls
    ></audio>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

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

function onTimeUpdate(event) {
  emit('timeUpdate', event.target.currentTime)
}

function onEnded() {
  emit('ended')
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