import _ from 'lodash'
import { defineStore } from 'pinia'

interface Face {
  id: number;
  image: string;
  skin_color: string;
}

interface UserScore {
  image: number;
  numeric: number;
  sentiment: string | null;
}

interface UserEmotion {
  // Define your structure here
}

interface ImagesState {
  faces: Face[];
  currentLevel: number;
  currentIndex: number;
  userScores: UserScore[];
  userEmotions: UserEmotion[];
}

const useImages = defineStore("images", {
  state: (): ImagesState => ({
    faces: [],
    currentLevel: 1,
    currentIndex: 0,

    userScores: [],
    userEmotions: [],
  }),
  getters: {
    /**
     * Returns the current face based on the current
     * image index above
     *
     * @returns {Face | undefined} The current face
     */
    currentFace(): Face {
      return this.faces[this.currentIndex];
    },
    /**
     * @returns {Number} The number of images in the batch
     */
    numberOfImages(): number {
      return this.faces.length;
    },
    /**
     * @returns {Boolean} Whether the session was completed
     */
    isCompleted(): boolean {
      return this.currentLevel === 2 && this.currentIndex === 11;
    },
  },
  actions: {
    /**
     * Increases the current image index by 1
     */
    increaseIndex(): void {
      if (!this.isCompleted) {
        console.log("Increase index", this.currentIndex);
        this.currentIndex = this.currentIndex + 1;
      }
    },
    /**
     * Adds a score to a given face
     *
     * @param {Number} score The score to add. Should be between 1 and 5
     */
    addScore(score: number): void {
      this.userScores.push({
        image: this.currentFace.id,
        numeric: score,
        sentiment: null,
      });
    },
    /**
     *
     * Adds the sentiment to a face that has already been
     * evaluated by the user
     *
     * @param {string} sentiment Sentiment to add to a face
     */
    addSentiment(sentiment: string): void {
      const face = _.find(this.userScores, { image: this.currentFace.id });
      console.log("Face", face);
      if (face) {
        face.sentiment = sentiment;
      }
    },
    /**
     *
     * @param {string} feeling
     */
    addFeeling(feeling: string): void {
      feeling;
    },
    /**
     *
     * @param {string} color
     */
    addColor(color: string): void {
      color;
    },
  },
});

export {
  useImages
}
