<template>
  <section id="session">
    <v-card>
      <v-card-text>
        <v-autocomplete v-model="requestData.country" :items="listOfCountries" variant="solo-filled" flat auto-select-first solo hide-details>
          <v-text-field label="Country" />
        </v-autocomplete>

        <v-btn variant="tonal" color="primary" flat class="my-3">
          Date of birth: {{ requestData.date_of_birth }}

          <v-menu :close-on-content-click="false" activator="parent">
            <v-date-picker v-model="requestData.date_of_birth" :max="minimumDate" show-adjacent-months />
          </v-menu>
        </v-btn>

        <v-autocomplete v-model="requestData.ethnicity" :items="['Black', 'White']" variant="solo-filled" flat auto-select-first solo>
          <v-text-field label="Ethnicity" />
        </v-autocomplete>

        <v-autocomplete v-model="requestData.gender" :items="['Woman', 'Man', 'Other']" variant="solo-filled" class="my-2" flat auto-select-first solo>
          <v-text-field label="Gender" />
        </v-autocomplete>

        <v-btn :to="{ name: 'scoring' }" @click="requestNewSession">
          Continue
        </v-btn>
      </v-card-text>
    </v-card>
  </section>
</template>

<script setup lang="ts">
import countriesData from '@/data/countries.json'
import { useAxiosClient } from '@/plugins/client'
import { useLocalStorage } from '@vueuse/core'
import dayjs from 'dayjs'
import { onMounted, ref } from 'vue'

const listOfCountries = ref<string[]>([])

const { client } = useAxiosClient()
const scoringSession = useLocalStorage('scoringSession', null, {
  serializer: {
    read(raw) {
      return JSON.parse(raw)
    },
    write(value) {
      return JSON.stringify(value)
    }
  }
})

const countries = useLocalStorage<string[]>('countries', null, {
  serializer: {
    read(raw) {
      return JSON.parse(raw)
    },
    write(value) {
      return JSON.stringify(value)
    }
  }
})

function getCountries() {
  countries.value = countriesData.map(x => x.name.common)
}

const currentDate = dayjs()
const minDateResult = currentDate.subtract(18, 'year')
const minimumDate = ref(`${dayjs(minDateResult.toISOString()).year()}-12-31`)

const requestData = ref({
  country: 'France',
  gender: 'Woman',
  ethnicity: 'Black',
  date_of_birth: `${minDateResult.year()}-12-31`
})

async function newSession() {
  try {
    const response = await client.post('/faces/session', requestData.value)
    scoringSession.value = response.data.session
    return response.data
  } catch (e) {
    console.log(e)
    return null
  }
}

/**
 *
 */
async function requestNewSession() {
  try {
    if (scoringSession.value) {
      const response = await client.get(`/faces/session/${scoringSession.value}`)

      if (response.data.session_expired) {
        await newSession()
      }
    } else {
      await newSession()
    }
  } catch (e) {
    console.log(e)
  }
}

onMounted(() => {
  getCountries()
})
</script>
