<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Scoring</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Tab 1</ion-title>
        </ion-toolbar>
      </ion-header>

      <ion-row>
        <ion-col size="12">
          Index: {{ currentIndex }}, Level: {{ currentLevel}}
        </ion-col>
        <ion-col size="12">
          <ion-img :src="imagePath"></ion-img>
        </ion-col>
        <ion-col size="12">
          <ion-button v-if="imagesStore.isCompleted" @click="requestSaveScores">Finalize</ion-button>
          <div v-else class="scoring">
            <scoring-box @score-selected="handleScoreSelection"></scoring-box>
            <sentiment-box @score-selected="handleScoreSelection"></sentiment-box>
            <feeling-box @score-selected="handleScoreSelection"></feeling-box>
          </div>
        </ion-col>
      </ion-row>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { client } from '@/plugins/client';
import { useVueLocalStorage } from '@/plugins/vue-storages';
import { useImages } from '@/store/images';
import { IonButton, IonCol, IonContent, IonHeader, IonImg, IonPage, IonRow, IonTitle, IonToolbar } from '@ionic/vue';
import { storeToRefs } from 'pinia';
import { computed, onBeforeMount } from 'vue';
import { useRouter } from 'vue-router';

import FeelingBox from '@/components/scoring/FeelingBox.vue';
import ScoringBox from '@/components/scoring/ScoringBox.vue';
import SentimentBox from '@/components/scoring/SentimentBox.vue';

const router = useRouter()
const { data, instance } = useVueLocalStorage()

const imagesStore = useImages()
const { faces, currentFace, currentIndex, currentLevel } = storeToRefs(imagesStore)

/**
 * Gets a random list of faces to evaluate for the
 * actual scoring session
 */
const requestFaces = async function () {
  try {
    // We are running multiple scoring methods on the same images. So there is no
    // need to get a new set of faces on every page reload
    if (data.value.faces && data.value.faces.length > 0) {
      faces.value = data.value.faces
    } else {
      const response = await client.get('faces/random', { params: { size: 10 } })
      faces.value = response.data
      instance.create('faces', faces.value)
    }
  } catch (e) {
    console.log(e)
  }
}

/**
 * Save the scores from the user to the backend
 */
const requestSaveScores = async function () {
  try {
    const requestData = {
      'scores': imagesStore.userScores,
      'emotions': imagesStore.userEmotions
    }
    console.log(requestData)
    instance.create('faces', [])
    instance.create('userScores', [])
    instance.create('userEmotions', [])
    instance.create('currentIndex', 0)
    instance.create('currentLevel', 1)
    router.push({ name: 'home' })
  } catch (e) {
    console.log(e)
  }
}

/**
 * Updates the current image index in order to evaluate
 * the next face
 */
const handleScoreSelection = function () {
  imagesStore.increaseIndex()
}

onBeforeMount(() => {
  requestFaces()

  currentIndex.value = data.value.currentIndex || 0
  currentLevel.value = data.value.currentLevel || 1
  
  imagesStore.userScores = data.value.userScores || []
  imagesStore.userEmotions = data.value.userEmotions || []
})

const imagePath = computed(() => {
  if (currentFace.value?.image) {
    return currentFace.value.image
  } else {
    return 'https://placehold.co/300x300'
  }
})
</script>
