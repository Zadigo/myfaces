/*eslint no-unused-vars: "off"*/
/*eslint no-use-before-define: "off"*/

import { App, ComputedRef, Ref } from "vue";
import { GoogleAnalytics, GoogleAnalyticsOptions } from "./google_analytics";
import { TagManagerOptions } from "./google_tag_manager";

export let GoogleAnalyticsInstance: GoogleAnalytics | null;

interface WebAnalyticsOptions {
  useGa4?: Boolean;
  useTagManager?: Boolean;
  ga4Options?: GoogleAnalyticsOptions;
  tagManagerOptions?: TagManagerOptions;
}

declare function createWebAnalytics (options?: WebAnalyticsOptions): {
    install (app: App): void
}

declare function useGoogleAnalytics(): {
  analytics: GoogleAnalytics | null;
  datalayer: ComputedRef<Array>;
};
