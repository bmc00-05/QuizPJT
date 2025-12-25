<template>
  <div class="h-full w-full min-h-0 text-black flex flex-col gap-2">
    <div class="flex-1 min-h-0 flex flex-col gap-2">

      <!-- ✅ 위 50%: 스프라이트/스테이터스 2등분 -->
<div class="flex-1 min-h-0 grid gap-2 grid-cols-1 sm:grid-cols-[0.9fr_1.1fr]">
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
  <div class="pixel-panel__content h-full min-h-0 p-2 overflow-hidden">
    <Status class="h-full min-h-0" />
  </div>
</div>
      </div>

      <!-- ✅ 아래 50%: 메모장(전체) -->
      <div class="flex-1 min-h-0">
        <div class="pixel-panel h-full min-h-0">
          <div class="pixel-panel__content h-full min-h-0 p-2">
          <MemoPadInline
            v-if="accountStore.token"
            :apiUrl="API_URL"
            :token="accountStore.token"
            @openMyProblemSet="openMyProblem"
            @openHistory="openHistory"
            @openBadge="openBadge"
          />

          <!-- 토큰 없으면 안내/비활성 UI -->
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

const statusBox = ref(null)
const statusInner = ref(null)
const statusScale = ref(1)

// ✅ (원상복구 핵심) ResizeObserver 핸들러 선언
let ro1 = null
let ro2 = null

const fitStatus = async () => {
  // ✅ 항상 원본 크기 기준으로 재측정
  statusScale.value = 1
  await nextTick()

  const box = statusBox.value
  const inner = statusInner.value
  if (!box || !inner) return

  const bw = box.clientWidth
  const bh = box.clientHeight

  // ✅ transform이 아니라 “원본 콘텐츠” 크기
  const cw = inner.scrollWidth
  const ch = inner.scrollHeight

  if (!bw || !bh || !cw || !ch) return

  const s = Math.min(1, bw / cw, bh / ch)
  statusScale.value = Math.max(0.7, s)
}

const router = useRouter()
const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()

// ✅ 모달 상태
const historyOpen = ref(false)
const badgeOpen = ref(false)
const myProblemOpen = ref(false)

// (선택) 선택된 데이터
const selectedCoaching = ref(null)
const selectedBadge = ref(null)

// ✅ 유저 보장
const ensureUser = async () => {
  if (!accountStore.user) await accountStore.fetchMe?.()
}

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

// (선택) 라우팅으로 내 문제집 페이지로 가는 버튼
const goMyProblemSet = async () => {
  await ensureUser()
  router.push({ name: "myproblemset" })
}

onMounted(() => {
  fitStatus()

  // ✅ ResizeObserver가 없는 환경 대비
  if (typeof ResizeObserver !== "undefined") {
    ro1 = new ResizeObserver(fitStatus)
    ro2 = new ResizeObserver(fitStatus)

    if (statusBox.value) ro1.observe(statusBox.value)
    if (statusInner.value) ro2.observe(statusInner.value)
  }

  window.addEventListener("resize", fitStatus)
})

// ✅ 원래 있던 ensureUser onMounted 유지(원상복구)
onMounted(async () => {
  await ensureUser()
})

onBeforeUnmount(() => {
  window.removeEventListener("resize", fitStatus)
  ro1?.disconnect()
  ro2?.disconnect()
})
</script>

