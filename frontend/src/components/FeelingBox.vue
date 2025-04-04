<template>
  <div class="d-flex justify-space-around">
    <div id="permutation">
      <v-btn v-for="feeling in selectedPermutation" :key="feeling" class="me-2" color="dark" size="large" variant="tonal" rounded="3" @click="handleChangePermutation">
        <font-awesome-icon :icon="[ 'far', translatetToIcon(feeling)[1] ]" />
      </v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
// import { useFaces } from '@/store/images'
// import { storeToRefs } from 'pinia'
import { computed, ref } from 'vue'

type Permutations = string[][]

const permutations = [
  ['sad', 'neutral', 'smile'],
  ['neutral', 'sad', 'smile'],
  ['neutral', 'smile', 'sad'],
  ['smile', 'neutral', 'sad'],
  ['smile', 'sad', 'neutral'],
  ['sad', 'smile', 'neutral']
]

const emit = defineEmits({
  'score-selected'(_feeling: string) {
    return true
  }
})

// const imagesStore = useFaces()
// const { currentIndex } = storeToRefs(imagesStore)

const availablePermutations = ref<Permutations>(permutations)
const permutationIndex = ref(0)
const selectedPermutation = computed<['sad', 'neutral', 'sad']>(() => {
  return availablePermutations.value[permutationIndex.value]
})

/**
 *
 */
function translatetToIcon(feeling: 'sad' | 'neutral' | 'sad'): string[] {
  const mappingTable = {
    sad: ['md:emoticon-sad', 'face-frown'],
    neutral: ['md:emoticon-neutral', 'face-meh'],
    smile: ['md:emoticon-smile', 'face-smile']
  }
  return mappingTable[feeling]
}

/**
 *
 */
function handleChangePermutation(feeling: string) {
  const randomIndex = Math.floor(Math.random() * permutations.length)
  permutationIndex.value = randomIndex

  emit('score-selected', feeling)
}
</script>
