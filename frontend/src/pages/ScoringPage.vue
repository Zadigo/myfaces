<template>
  <section id="scoring">
    <v-card>
      <v-toolbar color="white">
        <v-toolbar-title class="text-h6">
          Face / Image: {{ currentIndex + 1 }} / Level: {{ currentLevel }}
          <v-btn @click="handleReconnection">
            Reconnect
          </v-btn>
          <v-btn @click="handleGetEmotions">
            Emotions
          </v-btn>
          <!-- <p>{{ evaluatedDate }}</p> -->
        </v-toolbar-title>

        <!-- <template #append>
          <v-menu transition="slide-x-transition">
            <template #activator="{ props }">
              <v-btn v-bind="props" icon="md:dots-vertical" />
            </template>

            <v-list>
              <v-list-item>Something</v-list-item>
            </v-list>
          </v-menu>
        </template> -->
      </v-toolbar>

      <v-card-text>
        <v-img :src="imagePath" :alt="`${currentFace?.skin_color} woman`" cover />

        <v-divider class="mt-4 mb-4" />

        <v-btn v-if="isCompleted">
          Finalize
        </v-btn>

        <div v-else class="scoring">
          <component :is="currentComponent" @score-selected="handleScoreSelection" @get-emotions="handleGetEmotions" />
        </div>
      </v-card-text>
    </v-card>
  </section>
</template>

<script setup lang="ts">
import { getWebsocketUrl, getDomain } from '@/plugins/client'
import { useFaces } from '@/store/images'
import { useStorage, useWebSocket } from '@vueuse/core'
import { storeToRefs } from 'pinia'
import { computed, markRaw, ref } from 'vue'

import type { WebsocketData, SendMessageData } from '@/types'

import FeelingBox from '@/components/FeelingBox.vue'
import ScoringBox from '@/components/ScoringBox.vue'
import SentimentBox from '@/components/SentimentBox.vue'

const sessionKey = useStorage<string>('sessionId', null)
const store = useFaces()
const { currentIndex, currentFace, currentLevel, sentiments } = storeToRefs(store)

const isCompleted = ref<boolean>(false)
// const emotions = ref<Emotions>([])

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
      break

    default:
      component = markRaw(ScoringBox)
      break
  }
  return component
})

function sendMessage(data: SendMessageData): string {
  return JSON.stringify(data)
}

const { data, send, status, open } = useWebSocket<string>(getWebsocketUrl('/ws/session'), {
  immediate: true,
  onConnected() {
    if (sessionKey.value) {
      send(sendMessage({ action: 'set.session_id', session_id: sessionKey.value }))
    } else {
      send(sendMessage({ action: 'get.session_id' }))
    }
    send(sendMessage({ action: 'random.face' }))
  },
  onMessage() {
    if (data.value) {
      const parsedData: WebsocketData = JSON.parse(data.value)

      if (parsedData.action === 'random.face') {
        console.log(parsedData)
        currentFace.value = parsedData.data
      }

      if (parsedData.action === 'get.session_id') {
        sessionKey.value = parsedData.token
      }

      if (parsedData.action === 'update.index') {
        if (parsedData.index) {
          currentIndex.value = parsedData.index
        }
      }

      if (parsedData.action === 'next.level') {
        if (parsedData.level) {
          currentLevel.value = parsedData.level
        }
      }

      if (parsedData.action === 'get.emotions') {
        console.log(parsedData)
        if (parsedData.level) {
          sentiments.value = parsedData.data
        }
      }
    }
  }
})

const imagePath = computed(() => {
  if (currentFace.value) {
    const domain = getDomain()
    return `${domain}media/${currentFace.value.image}`
  } else {
    return 'https://placehold.co/300x300'
  }
})

function handleScoreSelection(value: number | string) {
  console.log(value)
  if (currentFace.value) {
    send(sendMessage({
      action: 'save.score',
      face_id: currentFace.value.id,
      score: value
    }))
  }
}

function handleReconnection() {
  open()
  send(sendMessage({ action: 'random.face' }))
}

console.log(status.value)

// function handleRoundFinished() {}

function handleGetEmotions() {
  send(sendMessage({ action: 'get.emotions' }))
}
</script>
