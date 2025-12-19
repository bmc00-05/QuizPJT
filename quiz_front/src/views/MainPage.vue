<template>
  <div>
    <h1>메인 페이지</h1>
    <div>
      <span>유저 정보 로드   </span> 
        <span>| {{ username }} |</span>
        <span>Lv: {{ level }} |</span>
        <span>Exp: {{ exp }} |</span>
    </div>
  </div>
  <div>
    <RouterLink :to="{ name: 'map'}">
      메인 모드
    </RouterLink>
    <RouterLink :to="{ name: 'usermode'}">
      유저 모드
    </RouterLink>
    <RouterLink :to="{ name: 'profile', params: {'id':userId }}">
      유저 프로필
    </RouterLink>
    <RouterLink :to="{ name: 'ai'}">
      AI 코칭
    </RouterLink>
  </div>
  <RouterView/>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user';

const userStore = useUserStore()

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