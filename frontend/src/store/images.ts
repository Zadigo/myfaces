import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Face, Sentiments, SessionCache, UserScore } from '../types'

export const useFaces = defineStore('images', () => {
  const faces = ref<Face[]>([])
  const currentLevel = ref(2)
  const currentIndex = ref(0)
  const scoringCompleted = ref(0)
  const userScores = ref<UserScore[]>([])
  const userEmotions = ref<string[]>([])
  const currentFace = ref<Face>()
  const cache = ref<SessionCache>()

  const sentiments = ref<Sentiments>()
  const scores = ref<number[]>([])
  const sentimentsScores = ref<string[]>([])

  function addScore(value: number) {
    scores.value.push(value)
  }

  function addSentiment(value: string) {
    sentimentsScores.value.push(value)
  }

  return {
    addScore,
    addSentiment,
    sentiments,
    sentimentsScores,
    scores,
    faces,
    cache,
    currentLevel,
    currentIndex,
    scoringCompleted,
    userScores,
    userEmotions,
    currentFace
  }
})
