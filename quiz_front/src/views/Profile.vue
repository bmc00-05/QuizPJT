<template>
  <div class="h-full w-full min-h-0 text-black flex flex-col gap-2">
    <!-- ✅ 프로필 본문 -->
    <div class="flex-1 min-h-0">
      <div class="flex flex-col h-full min-h-0 gap-2">
        <!-- ✅ 위/아래 1:1 -->
        <div class="flex-1 min-h-0 grid grid-cols-2 gap-2">
          <!-- 스프라이트 -->
          <div class="relative min-h-0 overflow-hidden bg-black/5 rounded">
            <div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
              <SpriteSheet
                :src="idleSheet"
                :frameWidth="256"
                :frameHeight="256"
                :frames="8"
                :fps="8"
                :scale="1"
                class="block [image-rendering:pixelated]"
              />
            </div>
          </div>

          <!-- 스테이터스 -->
          <div class="pixel-panel">
            <div class="pixel-panel__content">
            <Status />
            </div>
          </div>

        </div>

        <!-- 아래 영역 -->
        <div
          class="flex-1 min-h-0 flex flex-col justify-center items-center gap-2 bg-black/5 rounded p-2"
        >
          <RouterLink :to="{ name: 'myproblemset' }" class="underline">
            내 문제 관리
          </RouterLink>

          <!-- ✅ 버튼 2개 -->
          <div class="flex gap-2">
            <button
              class="px-4 py-2 rounded border bg-white/70 hover:bg-white text-sm font-bold"
              @click="openHistory"
            >
              AI 코칭 히스토리
            </button>

            <button
              class="px-4 py-2 rounded border bg-white/70 hover:bg-white text-sm font-bold"
              @click="openBadge"
            >
              뱃지
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ✅ AI 히스토리 모달 -->
    <BaseModal v-if="historyOpen" @close="closeHistory">
      <AIHistory
        :apiUrl="API_URL"
        :token="accountStore.token"
        :endpoint="`/ai/feedback/history/`"
        @close="closeHistory"
        @select="onSelectCoaching"
      />
    </BaseModal>

    <!-- ✅ 뱃지 모달 -->
    <BaseModal v-if="badgeOpen" @close="closeBadge">
      <Badge
        :apiUrl="API_URL"
        :token="accountStore.token"
        @close="closeBadge"
        @select="onSelectBadge"
      />
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"

import idleSheet from "@/assets/character/test_sheet.png"
import SpriteSheet from "@/components/SpriteSheet.vue"
import Status from "@/components/Status.vue"

import BaseModal from "@/components/common/BaseModal.vue"
import AIHistory from "@/components/AIHistory.vue"
import Badge from "@/components/Badge.vue"

import { useAccountStore } from "@/stores/accounts"

const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()

// ✅ 모달 상태
const historyOpen = ref(false)
const badgeOpen = ref(false)

// (선택) 선택된 데이터 (가공 X)
const selectedCoaching = ref(null)
const selectedBadge = ref(null)

const ensureUser = async () => {
  if (!accountStore.user) {
    await accountStore.fetchMe?.()
  }
}

// ✅ AI 히스토리
const openHistory = async () => {
  await ensureUser()
  historyOpen.value = true
}
const closeHistory = () => {
  historyOpen.value = false
}
const onSelectCoaching = (item) => {
  selectedCoaching.value = item // ✅ 그대로
  historyOpen.value = false
}

// ✅ 뱃지
const openBadge = async () => {
  await ensureUser()
  badgeOpen.value = true
}
const closeBadge = () => {
  badgeOpen.value = false
}
const onSelectBadge = (item) => {
  selectedBadge.value = item // ✅ 그대로
  badgeOpen.value = false
}

onMounted(async () => {
  await ensureUser()
})
</script>
