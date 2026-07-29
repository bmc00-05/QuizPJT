import { defineStore } from "pinia"

import * as profileApi from "@/api/profile"

export const useProfileStore = defineStore("profile", {
  state: () => ({
    payload: null,      // status 응답 전체
    newBadges: [],      // new_badges만 따로 보관
    loading: false,
    error: null,
  }),

  actions: {
    async fetchMyStatus() {
      this.loading = true
      this.error = null
      try {
        const res = await profileApi.fetchStatus()
        this.payload = res.data
        this.newBadges = res.data?.new_badges ?? []
        return res.data
      } catch (e) {
        this.error = e?.response?.data ?? e?.message ?? "failed"
        throw e
      } finally {
        this.loading = false
      }
    },

    async ackNewBadges(codes) {
      await profileApi.ackNewBadges(codes)
      this.newBadges = []
    },
  },
})
