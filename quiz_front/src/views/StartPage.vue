<template>
  <div class="relative flex min-h-full flex-col">
    <div class="h-32 flex items-center justify-center">
      <h1>TITLE IMAGE</h1>
    </div>
    <div class="min-h-screen flex items-center justify-center flex-col">
    <RouterView />
    </div>
    <div class="absolute left-0 right-0 bottom-[25%] flex flex-col gap-4 px-6">
      <RouterLink v-if="!showMainButtons" :to="{ name: 'main' }" class="flex w-full justify-center">
        Press to Start
      </RouterLink>
    </div>
    <div v-if="showMainButtons" class="absolute left-0 right-0 bottom-[25%] flex flex-col gap-4 px-6">
      <RouterLink :to="{ name: 'login' }" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
        로그인
      </RouterLink>

      <RouterLink :to="{ name: 'signup' }" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
        회원가입
      </RouterLink>
    </div>
  </div>

  
  <!-- <div class="w-full h-32">
    <h1>TITLE IMAGE</h1>
  </div> -->
  <!-- <div class="mx-auto w-92">
    <RouterView />
  </div>
  <div v-if="showMainButtons" class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
    <RouterLink :to="{ name: 'login' }" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
      로그인
    </RouterLink>
    <br/>
    <RouterLink :to="{ name: 'signup' }" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
      회원가입
    </RouterLink>
    
    <RouterLink :to="{ name: 'main' }">
      Press to Start
    </RouterLink>
  </div> -->

</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
const route = useRoute()
const accountStore = useAccountStore()

const showMainButtons = computed(() =>
  !['login', 'signup'].includes(route.name) &&
  !accountStore.isLogin
)


</script>

<style scoped>

</style>