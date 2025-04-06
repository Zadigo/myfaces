<template>
  <div class="d-flex justify-space-around">
    <v-btn v-for="i in rankingMax" :key="i" color="dark" variant="tonal" rounded="3" @click="handleScoreSelection(i)">
      {{ i }}
    </v-btn>
  </div>
</template>

<script setup lang="ts">
import { useFaces } from '@/store/images'
import { ref } from 'vue'

const emit = defineEmits({
  'score-selected'(_score: number) {
    return true
  },
  'round-finished'(_action: string) {
    return true
  }
})

const store = useFaces()

const rankingMax = ref(5)

/**
 * Handles the action of adding a numerical
 * score to the given face
 */
function handleScoreSelection(score: number) {
  store.addScore(score)
  emit('score-selected', score)
}
</script>
