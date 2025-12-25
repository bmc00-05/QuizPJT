<template>
  <div class="h-full w-full min-h-0 text-black flex flex-col gap-2">
    <div class="flex-1 min-h-0 flex flex-col gap-2">
      <!-- ✅ 위 50%: 항상 2열 고정(배치 변경 없음) -->
      <div class="flex-1 min-h-0 grid gap-2 grid-cols-[minmax(0,0.9fr)_minmax(0,1.1fr)]">
        <!-- 스프라이트 -->
        <div
          ref="spriteBox"
          class="relative min-h-0 min-w-0 overflow-hidden bg-black/5 rounded"
        >
          <div class="absolute left-3/4 top-2/3 -translate-x-1/2 -translate-y-1/2">
            <SpriteSheet
              :src="idleSheet"
              :frameWidth="256"
              :frameHeight="256"
              :frames="8"
              :fps="8"
              :scale="spriteScale"
              class="block [image-rendering:pixelated]"
            />
          </div>
        </div>

        <!-- 스테이터스 -->
        <div class="pixel-panel h-full min-h-0 min-w-0 overflow-hidden">
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

  <BadgeCongratsModal
      v-if="showBadgeModal"
      :badges="badgesToShow"
      @close="closeBadgeModal"
    />

     <BaseModal v-if="congratsOpen" @close="congratsOpen = false">
      <div class="p-4 text-black">
        <div class="font-bold mb-2">🎉 뱃지 획득!</div>

        <div class="flex items-center gap-3">
          <img
            v-if="earnedIcon"
            :src="earnedIcon"
            class="w-14 h-14 [image-rendering:pixelated]"
            alt=""
          />
          <div>
            <div class="font-bold">{{ earned?.name }}</div>
            <div class="text-xs opacity-80">{{ earned?.description }}</div>
          </div>
        </div>

        <div class="mt-3 flex justify-end">
          <button class="px-3 py-2 border" @click="congratsOpen = false">
            확인
          </button>
        </div>
      </div>
    </BaseModal>
</template>


<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from "vue"
import { useRouter } from "vue-router"
import { useAccountStore } from "@/stores/accounts"
import { useProfileStore } from "@/stores/profile"
import BadgeCongratsModal from "@/components/BadgeCongratsModal.vue"

import idleSheet from "@/assets/character/test_sheet.png"
import SpriteSheet from "@/components/SpriteSheet.vue"
import Status from "@/components/Status.vue"

import MemoPadInline from "@/components/MemoPadInline.vue"
import BaseModal from "@/components/common/BaseModal.vue"
import AIHistory from "@/components/AIHistory.vue"
import Badge from "@/components/Badge.vue"
import MyProblemSetManager from "@/components/MyProblemSetManager.vue"
import { useUiStore } from "@/stores/ui"
const router = useRouter()
const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()
const profileStore = useProfileStore()

const showBadgeModal = ref(false)
const badgesToShow = computed(() => profileStore.newBadges)



const uiStore = useUiStore()

const congratsOpen = ref(false)
const earned = ref(null)

// (선택) 로컬 아이콘을 code로 매칭하고 싶으면 BadgeDex랑 똑같이
const badgeIcons = import.meta.glob("@/assets/badges/*.png", {
  eager: true,
  import: "default",
})

const resolveBadgeIcon = (code) => {
  if (!code) code = "default"
  const hit = Object.entries(badgeIcons).find(([path]) =>
    path.endsWith(`/assets/badges/${code}.png`)
  )
  if (hit) return hit[1]
  const fallback = Object.entries(badgeIcons).find(([path]) =>
    path.endsWith(`/assets/badges/default.png`)
  )
  return fallback ? fallback[1] : null
}

const earnedIcon = computed(() => {
  const code = earned.value?.code
  return resolveBadgeIcon(code) || earned.value?.icon || null
})

onMounted(() => {
  const b = uiStore.consumeEarnedBadge()
  if (b) {
    earned.value = b
    congratsOpen.value = true
  }
})


onMounted(async () => {
  // ✅ 홈(프로필) 진입 시 status 호출
  await profileStore.fetchMyStatus(accountStore.apiUrl, accountStore.token)

  // ✅ 새 배지 있으면 모달 오픈
  if (badgesToShow.value.length > 0) {
    showBadgeModal.value = true
  }
})

async function closeBadgeModal() {
  showBadgeModal.value = false

  // ✅ ack 호출(모달에서 실제로 보여준 codes만 보냄)
  const codes = badgesToShow.value.map(b => b.code)
  if (codes.length > 0) {
    await profileStore.ackNewBadges(accountStore.apiUrl, accountStore.token, codes)
  }
}

const ensureUser = async () => {
  if (!accountStore.user) await accountStore.fetchMe?.()
}

// ✅ 스프라이트 자동 축소(배치는 유지, 크기만 박스에 맞춤)
const spriteBox = ref(null)
const spriteScale = ref(1)
let roSprite = null

const fitSprite = async () => {
  await nextTick()
  const box = spriteBox.value
  if (!box) return

  const bw = box.clientWidth
  const bh = box.clientHeight
  if (!bw || !bh) return

  // SpriteSheet의 1배 크기 기준(256x256)
  const base = 256

  // 박스에 맞게 축소(여유 0.92)
  const s = Math.min(1, (bw / base) * 0.92, (bh / base) * 0.92)

  // 너무 작아지는 건 방지(원하면 0.5 → 0.4 등 조절)
  spriteScale.value = Math.max(0.55, s)
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
  await fitSprite()

  if (typeof ResizeObserver !== "undefined") {
    roSprite = new ResizeObserver(fitSprite)
    if (spriteBox.value) roSprite.observe(spriteBox.value)
  }

  window.addEventListener("resize", fitSprite)
})

onBeforeUnmount(() => {
  window.removeEventListener("resize", fitSprite)
  roSprite?.disconnect()
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
