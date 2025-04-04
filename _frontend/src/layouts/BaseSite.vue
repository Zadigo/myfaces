<template>
  <v-container>
    <v-row tag="section" class="my-5">
      <v-col cols="5" offset="4">
        <router-view />
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'BaseSite'
})
</script>
