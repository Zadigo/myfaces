/* eslint no-unused-vars: "off" */
/* eslint no-use-before-define: "off" */

import { BaseAnalytics } from './base'

interface TagManagerOptions {
  gtmId?: string
}

declare class GoogleTagManager extends BaseAnalytics {
  constructor(options?: TagManagerOptions)
}
