<template>
  <!-- ✅ 패널 자체가 화면 끝까지 -->
  <div class="pixel-panel w-full h-full min-h-0 flex flex-col text-black">
    <div v-if="rankData" class="pixel-panel__content flex-1 min-h-0 flex flex-col items-center">
      <!-- ✅ 헤더는 고정(스크롤 안 됨) -->
      <div class="w-full text-center text-xl font-bold py-3 shrink-0">
        Ranking Board
      </div>

      <!-- ✅ 리스트만 남은 공간 전부 + 여기만 스크롤 -->
      <div class="w-full flex-1 min-h-0 overflow-y-auto px-2 pb-3">
        <ul class="w-full max-w-[360px] mx-auto flex flex-col gap-2">
          <li
            v-for="rank in (rankData.items ?? [])"
            :key="rank.user_id"
            class="w-full flex items-center justify-between px-3 py-2 input-panel-icon"
            @click="openUser(rank.user_id)"
          >
            <span class="w-10 text-center font-bold">{{ rank.rank }}</span>
            <span class="flex-1 text-center">{{ rank.username }}</span>
            <span class="w-16 text-center">Lv {{ rank.level }}</span>
            <span class="w-24 text-right">{{ rank.total_experience }}</span>
          </li>
        </ul>
      </div>
    </div>

    <div v-else class="pixel-panel__content flex-1 min-h-0 flex items-center justify-center text-gray-500">
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
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'

import BaseModal from '@/components/common/BaseModal.vue'
import Status from '@/components/Status.vue'

const accountStore = useAccountStore()
const API_URL = import.meta.env.VITE_REST_API_URL

const rankData = ref(null)

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
</style>