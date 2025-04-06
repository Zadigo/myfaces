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
import { sessionCache } from '@/data'
import { useFaces } from '@/store/images'
import { useStorage } from '@vueuse/core'
import { useCookies } from '@vueuse/integrations/useCookies'
import { useRoute } from 'vue-router'
import { useAxiosClient } from '@/plugins/client'
import type { SessionCache } from '@/types'

import BaseSite from '@/layouts/BaseSite.vue'
import { onMounted } from 'vue'

const { client } = useAxiosClient()
const { get, set } = useCookies(['sessionKey'])
const route = useRoute()
const cache = useStorage<SessionCache>('cache', sessionCache)
const storeFaces = useFaces()

onMounted(async () => {
  const sessionKey = get('sessionKey')
  if (!sessionKey) {
    const response = await client.get<{ token: string }>('/v1/faces/session-key')
    set('sessionKey', response.data.token)
  }
})

storeFaces.$subscribe((_, state) => {
  if (state.cache) {
    cache.value = state.cache
  }
}, {
  detached: true
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,3000,4000,5000,7001,3001,4001,5001,700&display=swap')
</style>
