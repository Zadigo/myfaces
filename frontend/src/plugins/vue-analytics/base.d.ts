/* eslint no-unused-vars: "off" */
/* eslint no-use-before-define: "off" */

declare class BaseAnalytics {
  configured: boolean

  constructor(options): void

  createScriptBody(): string | null
}

export { BaseAnalytics }
