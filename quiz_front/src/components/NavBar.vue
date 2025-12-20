<template>
<nav
  class="h-16 w-full
        bg-gray-800 border-t border-gray-700
        flex justify-around items-center"
>
  <RouterLink :to="{ name: 'map'}" class="nav-btn">
    🗺️
    <span>메인</span>
  </RouterLink>

  <RouterLink :to="{ name: 'usermode'}" class="nav-btn">
    👤
    <span>유저</span>
  </RouterLink>

  <RouterLink :to="{ name: 'profile'}" class="nav-btn">
    ⭐
    <span>프로필</span>
  </RouterLink>

  <!-- <RouterLink  class="nav-btn"> -->
    🤖
    <span>AI</span>
  <!-- </RouterLink> -->
</nav>
</template>

<script setup>


</script>

<style scoped>

</style>