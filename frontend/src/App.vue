<template>
  <BaseSite>
    <v-app>
      <Transition>
        <router-view :key="route.name" />
      </Transition>
    </v-app>
  </BaseSite>
</template>

<script setup lang="ts">
import { sessionCache } from '@/data';
import { useFaces } from '@/store/images';
import { useSessionStorage } from '@vueuse/core';
import { useRoute } from 'vue-router';

import BaseSite from '@/layouts/BaseSite.vue';

const route = useRoute()

const cache = useSessionStorage('cache', sessionCache, {
  serializer: {
    read (raw) {
      return JSON.parse(raw)
    },
    write (value) {
      return JSON.stringify(value)
    }
  }
})

const storeFaces = useFaces()

console.log(storeFaces, cache)

// storeFaces.$subscribe(({ storeId }, state) => {
//   storeId
//   state
// })
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap');
</style>
