<template>
  <div class="d-flex justify-around flex-wrap">
    <v-btn v-for="sentiment in currentEmotions" :key="sentiment" color="dark" rounded="3" variant="tonal" class="me-2 mb-2" @click="handleSentimentSelection(sentiment)">
      {{ sentiment }}
    </v-btn>
  </div>
</template>

<script setup lang="ts">
import { useAxiosClient } from '@/plugins/client'
import { useFaces } from '@/store/images'
import { Emotions } from '@/types'
import { storeToRefs } from 'pinia'
import { computed, onBeforeMount, ref, watch } from 'vue'

const emit = defineEmits({
  'score-selected'(_sentiment: string) {
    return true
  }
})

const imagesStore = useFaces()
const { currentIndex } = storeToRefs(imagesStore)

const { client } = useAxiosClient()

const sentiments = ref<Emotions>()
const currentEmotions = ref<Emotions[]>([])

const positiveEmotions = computed(() => {
  if (sentiments.value) {
    return sentiments.value.positive
  } else {
    return []
  }
})

const negativeEmotions = computed(() => {
  if (sentiments.value) {
    return sentiments.value.negative
  } else {
    return []
  }
})

/**
 * Shuffles the selected emotions so that they are not
 * linear
 */
function shuffleEmotions(emotions: string[]): string[] {
  return emotions.sort(() => Math.random() - 0.5)
}

/**
 * Selects a random amount of emotions from the available list
 * of positive and negative emotions
 */
function getRandomEmotions(emotions: string[], size = 5): string[] {
  const shuffledArray = emotions.sort(() => Math.random() - 0.5)
  return shuffledArray.slice(0, size)
}

/**
 * This function generates a random equal sets of sentiments
 * for each the positive and negative ones for the user to
 * rate current given face
 */
function generateRandomSentiments() {
  const randomPositiveEmotions = getRandomEmotions(positiveEmotions.value)
  const randomNegativeEmotions = getRandomEmotions(negativeEmotions.value)
  const newEmotions = [...randomPositiveEmotions, ...randomNegativeEmotions]

  currentEmotions.value = shuffleEmotions(newEmotions)
}

/**
 *
 */
async function requestSentiments() {
  try {
    const response = await client.get('/faces/emotions')
    sentiments.value = response.data
    generateRandomSentiments()
  } catch {
    // Handle error
  }
}

/**
 * Function that handles the user's selection
 */
function handleSentimentSelection(sentiment: string) {
  imagesStore.addSentiment(sentiment)
  generateRandomSentiments()
  emit('score-selected', sentiment)
}

watch(currentIndex, (n, o) => {
  if (n !== o) {
    generateRandomSentiments()
  }
})

onBeforeMount(() => {
  requestSentiments()
})
</script>
