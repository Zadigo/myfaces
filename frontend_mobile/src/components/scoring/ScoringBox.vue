<template>
  <div class="">
    <ion-button v-for="i in rankingMax" :key="i" @click="handleScoreSelection(i)">
      {{ i }}
    </ion-button>
  </div>
</template>

<script setup lang="ts">
import { useImages } from '@/store/images';
import { IonButton } from '@ionic/vue';
import { ref } from 'vue';

const rankingMax = ref(5)
const imagesStore = useImages()
const scoreSelected = defineEmits(['scored-selected'])

const handleScoreSelection = function (score: number): void {
  imagesStore.addScore(score)
  scoreSelected('score-selected', score)
}
</script>
