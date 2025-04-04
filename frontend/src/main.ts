import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import { installPlugins } from './plugins'

import DayJsAdapter from '@date-io/dayjs'
import App from './App.vue'
import router from './router'

import './style.scss'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'mdb-ui-kit/css/mdb.min.css'
import 'vuetify/styles'

import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import colors from 'vuetify/util/colors'

const vuetify = createVuetify({
  components,
  directives,
  date: {
    adapter: DayJsAdapter,
  },
  theme: {
    themes: {
      light: {
        dark: false,
        colors: {
          primary: colors.red.darken1,
        },
      },
    },
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
})

const pinia = createPinia()

const app = createApp(App)

app.use(vuetify)
app.use(router)
app.use(installPlugins())
app.use(pinia)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.mount('#app')
