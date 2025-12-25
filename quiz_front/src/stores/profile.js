import { defineStore } from "pinia"
import axios from "axios"

export const useProfileStore = defineStore("profile", {
  state: () => ({
    payload: null,      // status 응답 전체
    newBadges: [],      // new_badges만 따로 보관
    loading: false,
    error: null,
  }),

  actions: {
    async fetchMyStatus(apiUrl, token) {
      this.loading = true
      this.error = null
      try {
        const res = await axios.get(`${apiUrl}/profiles/status/`, {
          headers: { Authorization: `Token ${token}` },
        })
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

    async ackNewBadges(apiUrl, token, codes) {
      // codes 없으면 전부 ack 처리도 가능하지만, 안전하게 codes 보내는 방식 추천
      await axios.post(
        `${apiUrl}/profiles/me/badges/ack/`,
        { codes },
        { headers: { Authorization: `Token ${token}` } }
      )
      this.newBadges = []
    },
  },
})
