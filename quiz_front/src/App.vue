<template>
  <div class="min-h-screen flex justify-center bg-neutral-900">
    <div class="w-full max-w-[420px] min-h-screen bg-amber-50">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style scoped>

</style>
