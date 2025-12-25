// src/stores/ui.js
import { defineStore } from "pinia"

export const useUiStore = defineStore("ui", {
  state: () => ({
    earnedBadge: null, // { id, code, name, description, icon } | null
  }),
  actions: {
    setEarnedBadge(badge) {
      this.earnedBadge = badge
    },
    consumeEarnedBadge() {
      const b = this.earnedBadge
      this.earnedBadge = null
      return b
    },
    clearEarnedBadge() {
      this.earnedBadge = null
    },
  },
})
