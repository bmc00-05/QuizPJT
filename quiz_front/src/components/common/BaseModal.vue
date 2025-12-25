<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- 배경 -->
    <div class="absolute inset-0 bg-black/50" @click="emitClose" />

    <!-- 모달 박스 -->
    <div
      class="relative z-10 w-full max-w-[360px]
             max-h-[calc(80vh-2rem)]
             box-border overflow-hidden
             pixel-panel flex flex-col"
      @click.stop
    >
      <!-- ✅ 닫기 버튼: 모달 박스 기준 우측 상단 absolute 고정 -->
      <button
        class="absolute top-3 right-3 z-30 w-8 h-8 flex items-center justify-center"
        @click="emitClose"
        aria-label="닫기"
      >
        <img
          :src="quitIcon"
          alt="닫기"
          class="w-full h-full [image-rendering:pixelated] select-none pointer-events-none"
          draggable="false"
        />
      </button>

      <!-- ✅ 닫기 버튼 공간 확보(컨텐츠가 버튼 뒤로 안 가게) -->

      <!-- 내용: 필요하면 스크롤 -->
      <div class="pixel-panel__content overflow-y-auto no-scrollbar p-3">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import quitIcon from "@/assets/icons/quit_icon.png"

const emit = defineEmits(["close"])
const emitClose = () => emit("close")
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>
