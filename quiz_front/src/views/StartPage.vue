<template>
  <div class="relative min-h-screen overflow-hidden flex flex-col">
    <div class="absolute inset-0 bg-start-bg bg-cover bg-center bg-no-repeat"></div>
    <div class="absolute inset-0 bg-black/30"></div>

    <div class="relative z-10 flex min-h-screen flex-col">
      <div class="min-h-screen flex items-center justify-center flex-col">
        <!-- ✅ 타이틀 로고 -->
        <div class="fixed mt-10 top-0 z-20 h-32 w-full flex items-center justify-center pointer-events-none">
          <img
            :src="titleLogo"
            alt="Title Logo"
            class="w-[min(92vw,400px)] h-auto object-contain [image-rendering:pixelated] select-none"
            draggable="false"
          />
        </div>

        <!-- 로그인/회원가입 모달 -->
        <Transition name="modal">
          <div
            v-if="$route.name === 'login' || $route.name === 'signup'"
            class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
          >
            <RouterView />
          </div>
        </Transition>
      </div>

      <!-- Press to Start -->
      <div
        v-if="showStartButton"
        @click="$router.push({ name: 'profile' })"
        class="fixed inset-0 z-10 flex items-end justify-center pb-[25%] cursor-pointer"
      >
        <span class="text-lg font-bold  animate-fade-blink">
          Press to Start
        </span>
      </div>

      <!-- 로그인/회원가입 버튼 -->
      <div
        v-if="showMainButtons"
        class="absolute left-0 right-0 bottom-[20%] z-10 flex flex-col gap-4 px-6"
      >
        <RouterLink
          :to="{ name: 'login' }"
          class="input-panel-icon w-full flex justify-center font-bold"
        >
          로그인
        </RouterLink>

        <RouterLink
          :to="{ name: 'signup' }"
          class="input-panel-icon w-full flex justify-center font-bold"
        >
          회원가입
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAccountStore } from "@/stores/accounts"

// ✅ 타이틀 로고 경로
import titleLogo from "@/assets/background/title_logo.png"

const route = useRoute()
const accountStore = useAccountStore()
useRouter()

const showMainButtons = computed(
  () => !["login", "signup"].includes(route.name) && !accountStore.isLogin
)

const showStartButton = computed(() => accountStore.isLogin)
</script>

<style scoped>
.bg-start-bg {
  background-image: url("@/assets/background/main_title_2.jpg");
}
</style>
