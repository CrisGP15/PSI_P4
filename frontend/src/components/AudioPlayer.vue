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
  emit('onTimeUpdate', audio.value.currentTime)
}

function emitEnded() {
  emit('onEnded')
}


watch(() => props.stopAudio, (shouldStop) => {
  if (!audio.value) return
  if (shouldStop) {
    audio.value.pause()
  } else {
    audio.value.play()
  }
})
</script>