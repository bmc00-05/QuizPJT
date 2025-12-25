<template>
  <div class="h-full w-full min-h-0 text-black flex flex-col gap-2">
    <div class="flex-1 min-h-0 flex flex-col gap-2">
      <!-- 위 50%: (기본 1열) / (XL 이상에서만 2열) -->
      <div class="flex-1 min-h-0 grid gap-2 grid-cols-1 xl:grid-cols-[0.9fr_1.1fr]">
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
        <div class="pixel-panel h-full min-h-0 overflow-hidden">
          <div class="pixel-panel__content h-full min-h-0 p-1 overflow-y-auto no-scrollbar">
            <Status />
          </div>
        </div>
      </div>

      <!-- 아래 50%: 메모장 -->
      <div class="flex-1 min-h-0">
        <div class="pixel-panel h-full min-h-0">
          <div class="pixel-panel__content h-full min-h-0 p-1 overflow-hidden">
            <MemoPadInline
              v-if="accountStore.token"
              :apiUrl="API_URL"
              :token="accountStore.token"
              @openMyProblemSet="openMyProblem"
              @openHistory="openHistory"
              @openBadge="openBadge"
            />

            <div v-else class="text-xs text-black/60">
              로그인 후 사용 가능합니다.
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- AI 히스토리 모달 -->
    <BaseModal v-if="historyOpen" @close="closeHistory">
      <AIHistory
        :apiUrl="API_URL"
        :token="accountStore.token"
        :endpoint="`/ai/feedback/history/`"
        @close="closeHistory"
        @select="onSelectCoaching"
      />
    </BaseModal>

    <!-- 뱃지 모달 -->
    <BaseModal v-if="badgeOpen" @close="closeBadge">
      <Badge
        :apiUrl="API_URL"
        :token="accountStore.token"
        @close="closeBadge"
        @select="onSelectBadge"
      />
    </BaseModal>

    <!-- 내 문제집 모달 -->
    <BaseModal v-if="myProblemOpen" @close="closeMyProblem">
      <MyProblemSetManager :showClose="true" @close="closeMyProblem" />
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { useAccountStore } from "@/stores/accounts"

import idleSheet from "@/assets/character/test_sheet.png"
import SpriteSheet from "@/components/SpriteSheet.vue"
import Status from "@/components/Status.vue"

import MemoPadInline from "@/components/MemoPadInline.vue"
import BaseModal from "@/components/common/BaseModal.vue"
import AIHistory from "@/components/AIHistory.vue"
import Badge from "@/components/Badge.vue"
import MyProblemSetManager from "@/components/MyProblemSetManager.vue"

const router = useRouter()
const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()

const ensureUser = async () => {
  if (!accountStore.user) await accountStore.fetchMe?.()
}

// 모달 상태
const historyOpen = ref(false)
const badgeOpen = ref(false)
const myProblemOpen = ref(false)

const selectedCoaching = ref(null)
const selectedBadge = ref(null)

// 내 문제집
const openMyProblem = async () => {
  await ensureUser()
  myProblemOpen.value = true
}
const closeMyProblem = () => {
  myProblemOpen.value = false
}

// 히스토리
const openHistory = async () => {
  await ensureUser()
  historyOpen.value = true
}
const closeHistory = () => {
  historyOpen.value = false
}
const onSelectCoaching = (item) => {
  selectedCoaching.value = item
  historyOpen.value = false
}

// 뱃지
const openBadge = async () => {
  await ensureUser()
  badgeOpen.value = true
}
const closeBadge = () => {
  badgeOpen.value = false
}
const onSelectBadge = (item) => {
  selectedBadge.value = item
  badgeOpen.value = false
}

// (선택) 라우팅
const goMyProblemSet = async () => {
  await ensureUser()
  router.push({ name: "myproblemset" })
}

onMounted(async () => {
  await ensureUser()
})
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>