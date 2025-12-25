import { defineStore } from "pinia"
import axios from "axios"
import { useAccountStore } from "@/stores/accounts"

export const useUserStore = defineStore("user", {
  state: () => ({
    loaded: false,

    username: "",
    level: 1,
    exp: 0,
    maxExp: 100,

    // ✅ 추가: 서버 응답에 있음
    totalExperience: 0,
    equippedBadgeId: null,
    equippedBadge: null, // { id, code, name, icon } or null
  }),

  getters: {
    expPercent(state) {
      const max = state.maxExp || 1
      return Math.min((state.exp / max) * 100, 100)
    },
  },

  actions: {
    // ✅ 프로필 응답을 store state로 반영(공통)
    applyProfile(data) {
      if (!data) return

      this.username = data.username ?? this.username
      this.level = data.level ?? this.level
      this.exp = data.exp ?? this.exp
      this.maxExp = data.max_exp ?? this.maxExp

      this.totalExperience = data.total_experience ?? this.totalExperience
      this.equippedBadgeId = data.equipped_badge_id ?? this.equippedBadgeId
      this.equippedBadge = data.equipped_badge ?? this.equippedBadge

      this.loaded = true
    },

    async fetchUser({ force = false } = {}) {
      if (this.loaded && !force) return

      const API_URL = import.meta.env.VITE_REST_API_URL
      const accountStore = useAccountStore()

      try {
        const res = await axios.get(`${API_URL}/profile/`, {
          headers: { Authorization: `Token ${accountStore.token}` },
        })

        this.applyProfile(res.data)
      } catch (e) {
        // 로딩 실패 시 loaded는 false 유지
        console.error(e)
        this.loaded = false
        throw e
      }
    },

    clearUser() {
      this.$reset()
    },

    // ✅ 퀴즈/세션 결과로 경험치/레벨 업데이트(서버 응답 형태가 다를 수 있어 안전하게)
    applySessionResult(result) {
      if (!result) return

      // 서버가 "after" 형태로 주면 우선 적용
      this.level = result.level_after ?? result.level ?? this.level
      this.exp = result.exp_after ?? result.experience ?? result.exp ?? this.exp
      this.maxExp = result.max_exp ?? result.maxExp ?? this.maxExp

      // 총 경험치/뱃지 변경이 세션 결과에 포함될 수도 있으니 처리
      if (result.total_experience != null) this.totalExperience = result.total_experience
      if (result.equipped_badge_id != null) this.equippedBadgeId = result.equipped_badge_id
      if (result.equipped_badge != null) this.equippedBadge = result.equipped_badge

      this.loaded = true
    },
  },
})
