<template>
  <section id="scoring">
    <v-card>
      <v-toolbar color="white">
        <v-toolbar-title class="text-h6">
          Face / Image: {{ currentIndex + 1 }} / Level: {{ currentLevel }}
          <p>{{ evaluatedDate }}</p>
        </v-toolbar-title>

        <template #append>
          <v-menu transition="slide-x-transition">
            <template #activator="{ props }">
              <v-btn v-bind="props" icon="md:dots-vertical" />
            </template>

            <v-list>
              <v-list-item>Something</v-list-item>
            </v-list>
          </v-menu>
        </template>
      </v-toolbar>
      
      <v-card-text>
        <v-img :src="imagePath" :data-iteration="currentIndex" :alt="`${currentFace?.skin_color} woman`" cover />

        <v-divider class="mt-4 mb-4" />
        
        
        <v-btn v-if="store.isCompleted" @click="requestSaveScores">
          Finalize
        </v-btn>

        <div v-else class="scoring">
          <!-- <scoring-box v-if="store.currentLevel === 1" @score-selected="handleScoreSelection" />
          <sentiment-box v-else-if="store.currentLevel === 2" @score-selected="handleScoreSelection" />
          <feeling-box v-else-if="store.currentLevel === 3" @score-selected="handleScoreSelection" /> -->

          <component :is="currentComponent" @score-selected="handleScoreSelection" @round-finished="handleRoundFinished" />
        </div>
      </v-card-text>
    </v-card>
  </section>
</template>

<script setup lang="ts">
import { getBaseUrl } from '@/plugins/client'
import { useFaces } from '@/store/images'
import { Emotions, Face, WSFaceResponse } from '@/types'
import { useWebSocket, whenever } from '@vueuse/core'
import { storeToRefs } from 'pinia'
import { computed, markRaw, onBeforeMount, ref } from 'vue'

import FeelingBox from '@/components/FeelingBox.vue'
import ScoringBox from '@/components/ScoringBox.vue'
import SentimentBox from '@/components/SentimentBox.vue'

const store = useFaces()
const { faces, currentFace, currentIndex, currentLevel } = storeToRefs(store)

const sentiments = ref<Emotions>()
const evaluatedDate = ref(null)


function sendMessage (data: Record<string, string>): string {
  return JSON.stringify(data)
}

const reachedFinalImage = computed(() => {
  return currentIndex.value >= 11
})

whenever(reachedFinalImage, () => {
  if (currentLevel.value === 2) {
    return 
  }

  if (currentLevel.value === 1) {
    currentIndex.value = 0
    currentLevel.value = 2
  }
})

const { data, send } = useWebSocket(getBaseUrl('/ws/session', null, true, 8000), {
  immediate: true,
  onConnected () {
    send(sendMessage({'type': 'get.faces'}))
  },
  onMessage () {
    const dataObj = JSON.parse(data.value)

    if (dataObj.type === 'update.time') {
      evaluatedDate.value = dataObj.date
    }

    if (dataObj.type === 'get.faces') {
      const data = dataObj as WSFaceResponse
      faces.value = data.results as Face[]
    }

    if (dataObj.type === 'get.emotions') {
      sentiments.value = dataObj as Emotions
    }
  }
})

// const unsubscribe = store.$subscribe((change) => {
//   console.log(change)
//   if (change.events.key === 'currentIndex') {
//     // TODO: 11 is just for testing, we should
//     // be running the whole image batch
//     if (store.currentIndex >= 11) {
//       store.currentLevel = 2
//       store.currentIndex = 0
//     }

//     // if (store.currentIndex === 11 && store.currentLevel === 2) {
//     //   // store.currentLevel = 3
//     //   // store.currentIndex = 0
//     // }
//   }
// })
// onUnmounted(unsubscribe)

const imagePath = computed(() => {
  if (currentFace.value) {
    return `http://127.0.0.1:8000/media/${currentFace.image}`
  } else {
    return 'https://placehold.co/300x300'
  }
})

const currentComponent = computed(() => {
  let component

  switch (currentLevel.value) {
    case 1:
      component = markRaw(ScoringBox)
      break

    case 2:
      component = markRaw(SentimentBox)
      break

    case 3:
      component = markRaw(FeelingBox)
      break;
  
    default:
      component = markRaw(ScoringBox)
      break
  }
  return component
})

/**
 * Gets a random list of faces to evaluate for the
 * actual scoring session
 */
// async requestFaces () {
//   try {
//     // We are running multiple scoring methods on the same images. So there is no
//     // need to get a new set of faces on every page reload
//     if (this.localStorageData.faces && this.localStorageData.faces.length > 0) {
//       this.faces = this.localStorageData.faces
//     } else {
//       const response = await this.$http.get<Face[]>('faces/random', { params: { size: 10 } })
//       this.faces = response.data
//       this.$localstorage.create('faces', this.faces)
//     }
//   } catch (e) {
//     console.log(e)
//   }
// },
/**
 * Save the scores from the user to the backend
 */
 function requestSaveScores () {
  send(sendMessage({'type': 'save.scores'}))
 }

// async requestSaveScores () {
//   try {
//     const requestData = {
//       'scores': this.store.userScores,
//       'emotions': this.store.userEmotions
//     }
//     console.log(requestData)
//     this.$localstorage.create<Face[]>('faces', [])
//     this.$localstorage.create<UserScore[]>('userScores', [])
//     this.$localstorage.create('userEmotions', [])
//     this.$localstorage.create('currentIndex', 0)
//     this.$localstorage.create('currentLevel', 1)
//     this.$router.push({ name: 'home' })
//   } catch (e) {
//     console.log(e)
//   }
// },
/**
 * Updates the current image index in order to evaluate
 * the next face
 */
function handleScoreSelection () {
  store.increaseIndex()
}

function handleRoundFinished (action: 'scores' | 'sentiment') {
  send(sendMessage({
    'type': 'round.finished',
    'action': action,
    'scores': store.userScores
  }))
}

onBeforeMount(() => {
  // In case the page reloads, we have the possibility to
  // reload what the user has already done and resume
  // this.requestFaces()

  // this.currentIndex = this.localStorageData.currentIndex || 0
  // this.currentLevel = this.localStorageData.currentLevel || 1
  
  // this.store.userScores = this.localStorageData.userScores || []
  // this.store.userEmotions = this.localStorageData.userEmotions || []
})
</script>
