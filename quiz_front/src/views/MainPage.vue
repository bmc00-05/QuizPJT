<template>
  <div>
    <h1>메인 페이지</h1>
    <RouterLink :to="{ name: 'map'}">
      스토리모드
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
import { ref } from 'vue'

const userId = ref(1)
</script>

<style scoped>

</style>