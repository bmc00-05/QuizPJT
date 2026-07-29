<template>
  <!--
    h-[100dvh] : 모바일 브라우저 주소창 변화를 반영하는 동적 뷰포트 높이.
                 100vh 는 주소창을 무시해 하단이 잘리거나 스크롤이 생긴다.
    min-w 제거 : 420px 를 강제하면 375px(iPhone SE) 360px(갤럭시) 등
                 대부분의 폰에서 가로 스크롤이 발생한다.
    safe-area  : 노치와 홈 인디케이터를 피한다 (viewport-fit=cover 와 함께 동작).
  -->
  <div class="h-[100dvh] flex justify-center bg-neutral-900">
    <div
      class="w-full max-w-[420px] h-full bg-amber-50 overflow-hidden
             pt-[env(safe-area-inset-top)] pb-[env(safe-area-inset-bottom)]"
    >
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
