import type { App } from 'vue'

import './fonts'

export function installPlugins () {
    return {

        install (app: App) {
            console.log(app)
        }
    }
}
