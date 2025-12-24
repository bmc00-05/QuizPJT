<template>
  <div class="h-screen flex flex-col text-white min-h-0">

    <!-- ✅ 상단 상태창(배경 적용 제외) -->
    <div class="nav-panel shrink-0 bg-black">
      <div class="pixel-panel__content flex items-center justify-between">
        <div>
          <span class="font-bold text-xl">Lv.{{ level }}</span> 
          <span> {{ username }} </span>
          <span class="bg-black">뱃지</span>
          <span>Exp: {{ exp }} |</span>
        </div>

        <button
          class="px-3 py-1 border rounded bg-white/10 hover:bg-white/20"
          @click="openMenu"
        >
          ☰
        </button>
      </div>
    </div>

    <!-- ✅ 중앙 영역만 9-slice 배경 -->
    <div
      class="flex-1 min-h-0 relative nine-bg"
      :style="{ '--nine-bg': `url(${nineBg})` }"
    >
      <!-- ✅ 내용은 프레임 위로 올라오게 -->
      <div class="nine-content h-full min-h-0 overflow-hidden p-2">
        <RouterView v-slot="{ Component, route }">
          <component :is="Component" :key="route.fullPath" />
        </RouterView>

        <Transition name="route-dim">
          <div v-if="isTransitioning" class="absolute inset-0 bg-black z-50 pointer-events-none" />
        </Transition>
      </div>
    </div>

    <!-- ✅ 하단 내비바(배경 적용 제외) -->
    <NavBar class="shrink-0" />

    <BaseModal v-if="isMenuOpen" @close="closeMenu">
      <LogoutConfirmModal @close="closeMenu" @logout="onLogout" />
    </BaseModal>
  </div>
</template>

<script setup>
import nineBg from "@/assets/background/blue-background.png" // ✅ 너 파일 경로로 바꿔줘

import { ref, onMounted, onBeforeUnmount } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useAccountStore } from '@/stores/accounts'

import NavBar from '@/components/NavBar.vue'
import BaseModal from '@/components/common/BaseModal.vue'
import LogoutConfirmModal from '@/components/LogoutConfirmModal.vue'

const userStore = useUserStore()
const accountStore = useAccountStore()
const router = useRouter()

const username = userStore.username
const level = userStore.level
const exp = userStore.exp

// ✅ 전역 modal store 대신 로컬 state 사용
const isMenuOpen = ref(false)

// ✅ 라우트 전환 오버레이 상태
const isTransitioning = ref(false)

// ✅ 라우터 가드 등록/해제용
let removeBefore = null
let removeAfter = null

onMounted(() => {
  userStore.fetchUser()

  // 이동 시작 -> 즉시 어둡게
  removeBefore = router.beforeEach((to, from, next) => {
    isTransitioning.value = true
    next()
  })

  // 이동 완료 -> 서서히 밝아지게(오버레이 제거)
  removeAfter = router.afterEach(() => {
    setTimeout(() => {
      isTransitioning.value = false
    }, 50)
  })
})

onBeforeUnmount(() => {
  // ✅ 중복 등록 방지(중요)
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
.nine-bg{
  position: relative;
  background: #6b7280; /* fallback */
  isolation: isolate;  /* ✅ 레이어 충돌 방지(중요) */
}

/* ✅ 9-slice 레이어는 아래(z-index:0) */
.nine-bg::before{
  content:"";
  position:absolute;
  inset:0;
  z-index: 0;          /* ✅ 아래로 */
  pointer-events:none;

  border-style: solid;
  border-width: 128px;              /* 이미지 테두리 두께와 맞추기 */
  border-image-source: var(--nine-bg);
  border-image-slice: 8 fill;
  border-image-width: 12px;
  border-image-repeat: stretch;
}

/* ✅ 실제 내용은 위(z-index:1) */
.nine-content{
  position: relative;
  z-index: 1;
}


/* 기존 route-dim 트랜지션은 그대로 */
.route-dim-enter-from,
.route-dim-leave-to { opacity: 0.2; }
.route-dim-enter-to,
.route-dim-leave-from { opacity: 1; }
.route-dim-enter-active { transition: opacity 0ms; }
.route-dim-leave-active { transition: opacity 800ms ease-out; }
</style>
