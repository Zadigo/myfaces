import { BaseAnalytics } from './base'

class GoogleAnalytics extends BaseAnalytics {
  constructor(options) {
    super(options)

    const defaultOptions = {
      debug: false, 
      analyticsId: null,
      disablePageView: false,
      currency: 'EUR'
    }
    const { debug, analyticsId } = options || defaultOptions

    const url = `https://www.googletagmanager.com/gtag/js?id=${analyticsId}`
    const scriptElement = document.createElement('script')
    scriptElement.src = url

    const asyncAttribue = document.createAttribute('async')
    scriptElement.setAttributeNode(asyncAttribue)

    document.head.appendChild(scriptElement)

    this.createScriptBody(analyticsId, debug)
    this.configured = true
    this.analyticsId = analyticsId
  }

  createScriptBody (id, debug) {
    const scriptElement = document.createElement('script')
    let configText

    if (debug) {
      configText = `gtag('config', '${id}', { debug: 'true' });`
    } else {
      configText = `gtag('config', '${id}');`
    }

    scriptElement.innerHTML = `
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    ${configText}`
    document.head.appendChild(scriptElement)
  }

  pageView () {
    
  }

  sendUserId (id) {
    window.gtag('config', this.analyticsId, {
      'user_id' : id
    })
  }

  exception (exception) {
    window.gtag('event', 'exception', exception)
  }
}

export {
  GoogleAnalytics
}
