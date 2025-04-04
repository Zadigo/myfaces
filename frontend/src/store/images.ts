import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import type { Face, SessionCache, UserScore } from '../types'

const NUMBER_OF_LEVELS = 2

// const NUMBER_OF_IMAGES = 10

export const useFaces = defineStore('images', () => {
  const faces = ref<Face[]>([])
  const currentLevel = ref(1)
  const currentIndex = ref(0)
  const scoringCompleted = ref(0)
  const userScores = ref<UserScore[]>([])
  const userEmotions = ref<string[]>([])

  const cache = ref<SessionCache>()

  const count = computed(() => {
    return faces.value.length
  })

  const currentFace = computed((): Face => {
    return faces.value[currentIndex.value]
  })

  const nextFace = computed((): Face | null => {
    const nextIndex = currentIndex.value + 1

    if (nextIndex > faces.value.length) {
      return null
    } else {
      return faces.value[nextIndex]
    }
  })

  const isCompleted = computed((): boolean => {
    return currentLevel.value === NUMBER_OF_LEVELS && (currentIndex.value + 1) === count.value
  })

  /**
   * Checks whether the image is the last image
   * for the current round
   */
  const isLastImageOfRound = computed(() => {
    return (currentIndex.value + 1) === count.value
  })

  const percentageComplete = computed(() => {
    return scoringCompleted.value / (count.value * NUMBER_OF_LEVELS)
  })

  function addScore(score: number) {
    userScores.value.push({
      image: currentFace.value.id,
      numeric: score,
      sentiment: null
    })
  }

  function addSentiment(sentiment: string) {
    const face = userScores.value.find(x => x.image === currentFace.value.id)

    if (face) {
      face.sentiment = sentiment
    } else {
      // Handle missing faace
    }

    userEmotions.value.push(sentiment)
  }

  function addFeeling(feeling: string) {
    console.log(feeling)
  }

  function addColor(color: string) {
    console.log(color)
  }

  function increaseLevel() {
    const level = currentLevel.value += 1

    if (!isCompleted.value) {
      currentIndex.value = 0
      currentLevel.value = level
    }
  }

  function increaseIndex() {
    const index = currentIndex.value += 1

    scoringCompleted.value += 1

    if (index < (count.value)) {
      currentIndex.value = index
    } else {
      increaseLevel()
    }
  }

  return {
    cache,
    addScore,
    addSentiment,
    addFeeling,
    addColor,
    increaseIndex,
    increaseLevel,
    currentFace,
    nextFace,
    isCompleted,
    isLastImageOfRound,
    percentageComplete,
    faces,
    currentLevel,
    currentIndex,
    scoringCompleted,
    userScores,
    userEmotions
  }
})
