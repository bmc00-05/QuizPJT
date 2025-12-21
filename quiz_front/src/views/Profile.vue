<template>
  <div>
    <h1>유저 정보 페이지</h1>

    <RouterLink :to="{ name: 'myproblemset'}">
      내 문제 관리
    </RouterLink>
  </div>
  <div class="flex items-center justify-center h-[220px]">
    <SpriteSheet
      :src="idleSheet"
      :frameWidth="128"
      :frameHeight="128"
      :frames="8"
      :fps="8"
      :scale="2"
    />
  </div>
</template>

<script setup>
import idleSheet from "@/assets/character/Test_animation-Sheet.png";
import SpriteSheet from "@/components/SpriteSheet.vue";



</script>

<style scoped>

</style>