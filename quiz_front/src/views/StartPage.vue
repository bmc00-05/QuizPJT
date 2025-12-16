<template>
  <RouterView/>
  <div>
    <h1>초기 시작 화면</h1>
    <RouterLink :to="{ name: 'login'}">
      로그인
    </RouterLink>
    <RouterLink :to="{ name: 'signup'}">
      회원가입
    </RouterLink>
    <RouterLink :to="{ name: 'main'}">
      Press to Start
    </RouterLink>
  </div>
</template>

<script setup>

</script>

<style scoped>

</style>