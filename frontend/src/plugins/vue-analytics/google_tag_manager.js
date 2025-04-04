import { BaseAnalytics } from "./base"

class GoogleTagManager extends BaseAnalytics {
  constructor(options) {
    super(options)
    const { gtmId } = options

    const el = document.createElement('script')
    el.innerHTML = `
    (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer', '${gtmId}');
    `
    document.head.prepend(el)
    
    const noScriptEl = document.createElement('noscript')
    const iframeEl = document.createElement('iframe')
    iframeEl.src = `https://www.googletagmanager.com/ns.html?id=${gtmId}`
    iframeEl.height = 0
    iframeEl.width = 0
    iframeEl.style.display = 'none'
    iframeEl.style.visibility = 'hidden'
    noScriptEl.appendChild(iframeEl)
    document.body.prepend(noScriptEl)
  }
}

export {
  GoogleTagManager
}
