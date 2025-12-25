<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- 배경 -->
    <div class="absolute inset-0 bg-black/50" @click="emitClose" />

    <!-- 모달 박스 -->
    <div
      class="relative z-10 w-full max-w-[360px]
             max-h-[calc(80vh-2rem)]
             min-h-0
             box-border overflow-hidden
             pixel-panel flex flex-col"
      @click.stop
    >
      <!-- ✅ 닫기 버튼: 공중에 떠있는 absolute (공간 차지 0) -->
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

      <!-- ✅ slot 래퍼: 레이아웃 공간 확보 없음(=우측/상단 빈공간 안 생김) -->
      <div class="pixel-panel__content flex-1 min-h-0 overflow-hidden p-3 flex flex-col">
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
