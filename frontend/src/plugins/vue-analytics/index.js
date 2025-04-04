import { computed } from 'vue'
import { GoogleAnalytics } from './google_analytics'
import { GoogleTagManager } from './google_tag_manager'

let GoogleAnalyticsInstance

export function createWebAnalytics (options) {
  const defaultOptions = { 
    useGa4: true, 
    useTagManager: false, 
    ga4Options: {},
    tagManagerOptions: {}
  }
  const { useGa4, useTagManager, ga4Options, tagManagerOptions } = options || defaultOptions

  return {
    install: function (app) {
      if (useGa4) {
        const instance = new GoogleAnalytics(ga4Options)
        GoogleAnalyticsInstance = instance
        window.GoogleAnalytics = instance
        app.config.globalProperties.$analytics = instance
      }
      
      if (useTagManager) {
        const instance = new GoogleTagManager(tagManagerOptions)
        window.GoogleTagManager = instance
        app.config.globalProperties.$tagmanager = instance
      }
    } 
  }
}

export function useGoogleAnalytics () {
  const analytics = GoogleAnalyticsInstance
  const datalayer = computed(() => {
    return window.datalayer
  })

  return {
    datalayer,
    analytics
  }
}

export {
  GoogleAnalyticsInstance
}

