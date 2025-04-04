<template>
  <section id="home">
    <BCard style="width: 25rem; overflow: hidden">
      <template #content>
        <v-btn :to="{ name: 'session' }" color="primary" class="mt-4" rounded>
          Continue
        </v-btn>
      </template>
    </BCard>
  </section>
</template>

<script setup lang="ts">
// import { useHead } from '@unhead/vue'

// useHead({
//   title: 'Home'
// })
</script>
