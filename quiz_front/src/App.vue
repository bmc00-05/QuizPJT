<template>
  <div class="h-screen flex justify-center bg-neutral-900 overflow-x-auto">
    <div class="w-full max-w-[420px] min-w-[420px] h-screen bg-amber-50 overflow-hidden">
      <RouterView class="h-full" />
    </div>

    <!-- 전역 다이얼로그: 브라우저 alert / confirm 대체 -->
    <AppDialog />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import AppDialog from '@/components/common/AppDialog.vue'
</script>

<style scoped>

</style>
