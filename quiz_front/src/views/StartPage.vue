<template>
  <div class="relative flex min-h-full flex-col">
    <div class="min-h-screen flex items-center justify-center flex-col">
      <div class="fixed top-0 h-32 flex items-center justify-center">
        <h1>TITLE IMAGE</h1>
      </div>
      <!-- 로그인/회원가입 컴포넌트 라우터뷰 + 모달 트랜지션 -> 서서히 등장 -->
        <Transition name="modal">
          <div
            v-if="$route.name === 'login' || $route.name === 'signup'"
            class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
          >
            <RouterView />
          </div>
        </Transition>
    </div>
    <!-- Press to Start 메인 페이지 진입 버튼 -->
    <div v-if="showStartButton" @click="$router.push({ name: 'main' })"
          class="fixed inset-0 z-10 flex items-end justify-center pb-[25%] cursor-pointer">
      <RouterLink to="{ name: 'main' }" class="flex w-full justify-center">
        <span class="text-lg font-semibold animate-fade-blink">
          Press to Start
        </span>
      </RouterLink>
    </div>

    <div v-if="showMainButtons" class="absolute left-0 right-0 bottom-[20%] flex flex-col gap-4 px-6">
      <RouterLink :to="{ name: 'login' }" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
        로그인
      </RouterLink>

      <RouterLink :to="{ name: 'signup' }" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
        회원가입
      </RouterLink>
    </div>
  </div>

</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
const route = useRoute()
const accountStore = useAccountStore()
const router = useRouter()
const showMainButtons = computed(() =>
  !['login', 'signup'].includes(route.name) &&
  !accountStore.isLogin
)

const showStartButton = computed(() =>
  accountStore.isLogin
  )


</script>

<style scoped>

</style>