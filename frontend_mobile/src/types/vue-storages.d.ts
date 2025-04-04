import { VueLocalStorage } from "@/plugins/vue-storages";
import "vue-storages/base";

declare module 'vue-storages/base' {
  export interface storageData {
    faces?: Array<{ id: number; image: string; skin_color: string }>;
    currentIndex?: number;
    currentLevel?: number;
    userScores?: Array<{ image: number; numeric: number; sentiment: string | null }>;
    userEmotions?: any[];
  }

  export function useVueLocalStorage(): {
    data: Ref<storageData>;
    instance: VueLocalStorage
  };
}
