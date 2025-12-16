<template>
  <div>
    <h1>메인 페이지</h1>
    <RouterLink :to="{ name: 'map'}">
      스토리모드
    </RouterLink>
    <RouterLink :to="{ name: 'usermode'}">
      유저 모드
    </RouterLink>
  </div>
  <RouterView/>
</template>

<script setup>

</script>

<style scoped>

</style>