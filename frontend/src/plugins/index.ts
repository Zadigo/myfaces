import type { Plugin } from 'vue'

import './fonts'

export function installPlugins(): Plugin {
  return {
    install(app) {
      console.log(app)
    }
  }
}
