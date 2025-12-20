<template>
  <div class="h-screen flex flex-col bg-gray-500 text-white">

    <div class="flex-1 overflow-hidden flex flex-col">
      <h1>메인 페이지</h1>

      <div>
        <span>유저 정보 로드 </span>
        <span>| {{ username }} |</span>
        <span>Lv: {{ level }} |</span>
        <span>Exp: {{ exp }} |</span>
      </div>

      <div class="flex-1 overflow-y-auto mt-4">
        <RouterView />
      </div>
    </div>


    <NavBar />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user';
import { useModalStore } from '@/stores/modal';
import NavBar from '@/components/NavBar.vue';

const userStore = useUserStore()
const modal = useModalStore()

const userId = ref(1)

const username = userStore.username
const level = userStore.level
const exp = userStore.exp

onMounted(() => {
  userStore.fetchUser()
})
</script>

<style scoped>

</style>