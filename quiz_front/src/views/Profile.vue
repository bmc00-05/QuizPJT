<template>
  <div class="h-full w-full min-h-0 text-black flex flex-col gap-2">
    <div class="flex-1 min-h-0 flex flex-col gap-2">
      <!-- ✅ 위 50%: (기본 1열) / (XL 이상에서만 2열) -->
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
        <div ref="statusBox" class="pixel-panel h-full min-h-0 overflow-hidden">
          <!-- ✅ 모바일/태블릿: 초기화면 유지(스케일 1) + 넘치면 스크롤
               ✅ PC/큰 화면: fitStatus로 축소(overflow hidden) -->
          <div
            class="pixel-panel__content h-full min-h-0 p-1"
            :class="isUnderXL ? 'overflow-y-auto no-scrollbar' : 'overflow-hidden'"
          >
            <!-- ✅ 스케일 적용 래퍼(중요) -->
            <div
              ref="statusInner"
              class="origin-top-left w-max"
              :style="{ transform: `scale(${statusScale})` }"
            >
              <Status />
            </div>
          </div>
        </div>
      </div>

      <!-- ✅ 아래 50%: 메모장(전체) -->
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

    <!-- ✅ 내 문제집 모달 -->
    <BaseModal v-if="myProblemOpen" @close="closeMyProblem">
      <MyProblemSetManager :showClose="true" @close="closeMyProblem" />
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from "vue"
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

// ✅ Status Fit refs
const statusBox = ref(null)
const statusInner = ref(null)
const statusScale = ref(1)

// ✅ "초기화면처럼" 유지 기준: XL(>=1280px) 미만이면 스케일링 하지 않음
const isUnderXL = ref(true)
const updateBreakpoint = () => {
  isUnderXL.value = window.matchMedia("(max-width: 1279px)").matches
}

// ✅ ResizeObserver 핸들러
let ro1 = null
let ro2 = null

const fitStatus = async () => {
  // ✅ 모바일/태블릿(=초기화면 유지): 스케일 고정 1
  if (isUnderXL.value) {
    statusScale.value = 1
    return
  }

  // ✅ PC/큰 화면에서만 "박스에 맞게 축소"
  statusScale.value = 1
  await nextTick()

  const box = statusBox.value
  const inner = statusInner.value
  if (!box || !inner) return

  const bw = box.clientWidth
  const bh = box.clientHeight

  // ✅ 콘텐츠 원본 크기(넘치는 것까지 포함)
  const cw = inner.scrollWidth
  const ch = inner.scrollHeight
  if (!bw || !bh || !cw || !ch) return

  const s = Math.min(1, bw / cw, bh / ch)
  // ✅ 너무 작아지는 건 방지(원하면 0.8로 올려도 됨)
  statusScale.value = Math.max(0.75, s)
}

// ✅ 유저 보장
const ensureUser = async () => {
  if (!accountStore.user) await accountStore.fetchMe?.()
}

// ✅ 모달 상태
const historyOpen = ref(false)
const badgeOpen = ref(false)
const myProblemOpen = ref(false)

const selectedCoaching = ref(null)
const selectedBadge = ref(null)

// ✅ 내 문제집 모달
const openMyProblem = async () => {
  await ensureUser()
  myProblemOpen.value = true
}
const closeMyProblem = () => {
  myProblemOpen.value = false
}

// ✅ 히스토리
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

// ✅ 뱃지
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

const onResize = () => {
  updateBreakpoint()
  fitStatus()
}

onMounted(async () => {
  updateBreakpoint()
  await ensureUser()
  await fitStatus()

  if (typeof ResizeObserver !== "undefined") {
    ro1 = new ResizeObserver(fitStatus)
    ro2 = new ResizeObserver(fitStatus)

    if (statusBox.value) ro1.observe(statusBox.value)
    if (statusInner.value) ro2.observe(statusInner.value)
  }

  window.addEventListener("resize", onResize)
})

onBeforeUnmount(() => {
  window.removeEventListener("resize", onResize)
  ro1?.disconnect()
  ro2?.disconnect()
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
