<template>
  <div>{{ msg }}</div>
  <div>{{ b }}</div>
  <div>{{ w(1) }}</div>
  <div />
</template>

<script setup lang="ts">

import { ref } from 'vue';

const msg = ref('Hello')

function w(c: number) {
  // pass
  console.log(c)
}

const b = 1
</script>
