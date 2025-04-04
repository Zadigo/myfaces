/*eslint no-unused-vars: "off"*/
/*eslint no-use-before-define: "off"*/

import { BaseAnalytics } from "./base";

interface GoogleAnalyticsOptions {
  debug?: boolean;
  analyticsId?: string;
  disablePageView?: boolean;
  currency?: string;
}

interface ExceptionOptions {
    description?: string
    fatal?: boolean
}

declare class GoogleAnalytics extends BaseAnalytics {
  constructor(options?: GoogleAnalyticsOptions);

  pageView();
  sendUserId(id: number | string | unknown);
  exception(exception?: ExceptionOptions);
}

declare module "@vue/runtime-core" {
  export interface ComponentCustomProperties {
    $analytics: GoogleAnalytics;
  }
}
