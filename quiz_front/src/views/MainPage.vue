<template>
  <div class="h-screen flex flex-col text-white min-h-0">
    <!-- ✅ 상단 상태창 -->
    <div class="nav-panel shrink-0 bg-black">
      <div class="pixel-panel__content p-0 flex items-center gap-2 h-12 overflow-hidden whitespace-nowrap">
        <!-- ✅ 좌측: 뱃지 -->
        <div class="shrink-0">
          <div class="input-panel-icon px-2 py-1">
            <div class="pixel-panel__content p-1 w-10 h-10 flex items-center justify-center">
              <img
                v-if="badgeIconUrl"
                :src="badgeIconUrl"
                :alt="badgeName"
                class="w-8 h-8 [image-rendering:pixelated] select-none"
                draggable="false"
              />
              <span v-else class="text-[10px] opacity-60">NO</span>
            </div>
          </div>
        </div>

        <!-- 가운데 -->
        <div class="min-w-0 flex-1 flex items-center gap-2">
          <span class="shrink-0 font-bold text-lg">Lv.{{ level }}</span>
          <span class="min-w-0 truncate text-sm opacity-90">
            {{ username }}
          </span>
        </div>

        <!-- 오른쪽 -->
        <button
          class="shrink-0 input-panel-icon px-3 py-1 hover:bg-white/20"
          @click="openMenu"
        >
          설정
        </button>
      </div>
    </div>

    <!-- ✅ 중앙 영역만 9-slice 배경 -->
    <div
      class="flex-1 min-h-0 relative nine-bg"
      :style="{ '--nine-bg': `url(${nineBg})` }"
    >
      <div class="nine-content h-full min-h-0 overflow-hidden p-2">
        <RouterView v-slot="{ Component, route }">
          <component :is="Component" :key="route.fullPath" />
        </RouterView>

        <Transition name="route-dim">
          <div
            v-if="isTransitioning"
            class="absolute inset-0 bg-black z-50 pointer-events-none"
          />
        </Transition>
      </div>
    </div>

    <!-- ✅ 하단 내비바 -->
    <NavBar class="shrink-0" />

    <!-- ✅ 설정 모달 -->
    <BaseModal v-if="isMenuOpen" @close="closeMenu">
      <LogoutConfirmModal @close="closeMenu" @logout="onLogout" />
    </BaseModal>
  </div>
</template>

<script setup>
import nineBg from "@/assets/background/blue-background.png"

import { ref, onMounted, onBeforeUnmount, computed } from "vue"
import { RouterView, useRouter } from "vue-router"
import { storeToRefs } from "pinia"
import { useUserStore } from "@/stores/user"
import { useAccountStore } from "@/stores/accounts"

import NavBar from "@/components/NavBar.vue"
import BaseModal from "@/components/common/BaseModal.vue"
import LogoutConfirmModal from "@/components/LogoutConfirmModal.vue"

const userStore = useUserStore()
const accountStore = useAccountStore()
const router = useRouter()

// ✅ 스토어 반응성 유지
const { username, level, equippedBadge } = storeToRefs(userStore)

// ✅ 로컬 뱃지 폴더(빌드 포함): /src 경로로 glob 해야 안전함
// - 확장자 섞여도 대응하도록 패턴 확장
const badgeIcons = import.meta.glob("/src/assets/badges/*.{png,webp,jpg,jpeg}", {
  eager: true,
  import: "default",
})

// ✅ 서버 응답: equipped_badge.code 로 매칭
const badgeCode = computed(() => equippedBadge.value?.code ?? "default")
const badgeName = computed(() => equippedBadge.value?.name ?? "badge")

// ✅ code에 해당하는 로컬 파일을 찾아 URL 반환 (확장자 자동 탐색)
const badgeIconUrl = computed(() => {
  const code = badgeCode.value
  const exts = ["png", "webp", "jpg", "jpeg"]

  for (const ext of exts) {
    const key = `/src/assets/badges/${code}.${ext}`
    if (badgeIcons[key]) return badgeIcons[key]
  }

  for (const ext of exts) {
    const fallback = `/src/assets/badges/default.${ext}`
    if (badgeIcons[fallback]) return badgeIcons[fallback]
  }

  return null
})

const isMenuOpen = ref(false)
const isTransitioning = ref(false)

let removeBefore = null
let removeAfter = null

onMounted(() => {
  userStore.fetchUser()

  removeBefore = router.beforeEach((to, from, next) => {
    isTransitioning.value = true
    next()
  })

  removeAfter = router.afterEach(() => {
    setTimeout(() => {
      isTransitioning.value = false
    }, 50)
  })
})

onBeforeUnmount(() => {
  if (removeBefore) removeBefore()
  if (removeAfter) removeAfter()
})

const openMenu = () => {
  isMenuOpen.value = true
}

const closeMenu = () => {
  isMenuOpen.value = false
}

const onLogout = () => {
  accountStore.logOut()
  closeMenu()
}
</script>

<style scoped>
.nine-bg {
  position: relative;
  background: #6b7280;
  isolation: isolate;
}

.nine-bg::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;

  border-style: solid;
  border-width: 128px;
  border-image-source: var(--nine-bg);
  border-image-slice: 8 fill;
  border-image-width: 12px;
  border-image-repeat: stretch;
}

.nine-content {
  position: relative;
  z-index: 1;
}

.route-dim-enter-from,
.route-dim-leave-to { opacity: 0.2; }
.route-dim-enter-to,
.route-dim-leave-from { opacity: 1; }
.route-dim-enter-active { transition: opacity 0ms; }
.route-dim-leave-active { transition: opacity 800ms ease-out; }
</style>
