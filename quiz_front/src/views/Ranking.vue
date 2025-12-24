<template>
  <div class="pixel-panel w-full text-black">
    <div v-if="rankData" class="pixel-panel__content flex flex-col items-center">
      <div class="w-full text-center text-xl font-bold mb-4">
        Ranking Board
      </div>

      <ul class="w-full max-w-[360px] flex flex-col items-center gap-2">
        <li
          v-for="rank in (rankData.items ?? [])"
          :key="rank.user_id"
          class="w-full flex items-center justify-between px-3 py-2 bg-white/70 rounded border cursor-pointer hover:bg-white"
          @click="openUser(rank.user_id)"
        >
          <span class="w-10 text-center font-bold">{{ rank.rank }}</span>
          <span class="flex-1 text-center">{{ rank.username }}</span>
          <span class="w-16 text-center">Lv {{ rank.level }}</span>
          <span class="w-24 text-right">{{ rank.total_experience }}</span>
        </li>
      </ul>
    </div>

    <div v-else class="pixel-panel__content text-center text-gray-500">
      로딩중...
    </div>

    <!-- ✅ 유저 정보 모달 -->
    <BaseModal v-if="userModalOpen" @close="closeUserModal">
      <!-- Status.vue를 그대로 재사용 -->
      <div class="w-full max-w-[420px]">
        <div class="flex items-center justify-between mb-2">
          <div class="font-bold">유저 정보</div>
          <button class="underline text-sm" @click="closeUserModal">닫기</button>
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