<template>
  <!-- ✅ 패널 자체가 화면 끝까지 -->
  <div class="pixel-panel w-full h-full min-h-0 flex flex-col text-black">
    <div
      v-if="rankData"
      class="pixel-panel__content flex-1 min-h-0 flex flex-col items-center"
    >
      <!-- ✅ 헤더는 고정(스크롤 안 됨) -->
      <div class="w-full text-center text-xl font-bold py-3 shrink-0">
        Ranking Board
      </div>

      <!-- ✅ 컬럼 설명 바(고정) -->
      <div class="w-full shrink-0 px-2 pb-2">
        <div
          class="w-full max-w-[360px] mx-auto
                 flex items-center justify-between
                 px-3 py-2
                 input-panel-content border-black/20 bg-white/40
                 text-[11px] font-bold opacity-80"
        >
          <span class="w-10 text-center">RANK</span>
          <span class="flex-1 text-center">USER</span>
          <span class="w-16 text-center">LEVEL</span>
          <span class="w-24 text-right">TOTAL EXP</span>
        </div>
      </div>

      <!-- ✅ 리스트만 남은 공간 전부 + 여기만 스크롤 -->
      <div class="w-full flex-1 min-h-0 overflow-y-auto px-2 pb-3 no-scrollbar">
        <ul class="w-full max-w-[360px] mx-auto flex flex-col gap-2">
          <li
            v-for="rank in (rankData.items ?? [])"
            :key="rank.user_id"
            class="w-full flex items-center justify-between px-3 py-2 input-panel-icon"
            @click="openUser(rank.user_id)"
          >
            <span class="w-10 text-center font-bold">{{ rank.rank }}</span>

            <!-- ✅ USER + badge -->
            <span class="flex-1 flex items-center justify-center gap-2 min-w-0">
              <img
                v-if="badgeIconUrl(badgeCodeOf(rank))"
                :src="badgeIconUrl(badgeCodeOf(rank))"
                alt=""
                class="w-5 h-5 [image-rendering:pixelated] select-none shrink-0"
                draggable="false"
              />
              <span class="truncate">{{ rank.username }}</span>
            </span>

            <span class="w-16 text-center">Lv {{ rank.level }}</span>
            <span class="w-24 text-right">{{ rank.total_experience }}</span>
          </li>
        </ul>
      </div>
    </div>

    <div
      v-else
      class="pixel-panel__content flex-1 min-h-0 flex items-center justify-center text-gray-500"
    >
      로딩중...
    </div>

    <!-- ✅ 유저 정보 모달 -->
    <BaseModal v-if="userModalOpen" @close="closeUserModal">
      <div class="w-full max-w-[360px]">
        <div class="flex items-center justify-between mb-2">
          <div class="font-bold">유저 정보</div>
        </div>
        <Status :userId="selectedUserId" />
      </div>
    </BaseModal>
  </div>
</template>

<script setup>
import axios from "axios"
import { ref, onMounted } from "vue"
import { useAccountStore } from "@/stores/accounts"

import BaseModal from "@/components/common/BaseModal.vue"
import Status from "@/components/Status.vue"

const accountStore = useAccountStore()
const API_URL = import.meta.env.VITE_REST_API_URL

const rankData = ref(null)

// ✅ 로컬 뱃지 폴더의 png를 전부 포함 (src/assets/badge/*.png)
const badgeIcons = import.meta.glob("@/assets/badges/*.{png,PNG}", {
  eager: true,
  import: "default",
})

// ✅ 랭킹 row에서 뱃지 코드 꺼내기 (서버 필드명 맞춰 여기만 수정)
const badgeCodeOf = (rank) => {
  return (
    rank?.equipped_badge?.code ??
    rank?.equipped_badge_code ??
    rank?.badge_code ??
    rank?.badge ??
    null
  )
}

const badgeIconUrl = (code) => {
  if (!code) return null

  // vite glob key는 보통 "/src/assets/..." 형태라 endsWith로 안전하게 매칭
  const hit = Object.entries(badgeIcons).find(([path]) =>
    path.endsWith(`/assets/badges/${code}.png`) || path.endsWith(`/assets/badges/${code}.PNG`)
  )
  if (hit) return hit[1]

  // fallback (없으면 null로)
  const fallback = Object.entries(badgeIcons).find(([path]) =>
    path.endsWith(`/assets/badges/default.png`) || path.endsWith(`/assets/badges/default.PNG`)
  )
  return fallback ? fallback[1] : null
}

// ✅ 모달 상태
const userModalOpen = ref(false)
const selectedUserId = ref(null)

const openUser = (userId) => {
  selectedUserId.value = userId
  userModalOpen.value = true
}

const closeUserModal = () => {
  userModalOpen.value = false
  selectedUserId.value = null
}

const getRank = async () => {
  const res = await axios.get(`${API_URL}/profile/ranking/`, {
    headers: { Authorization: `Token ${accountStore.token}` },
  })
  rankData.value = res.data
}

onMounted(getRank)
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>
