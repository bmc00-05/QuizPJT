<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center">
    <!-- 배경 -->
    <div class="absolute inset-0 bg-black/50" @click="emitClose" />

    <!-- 모달 박스 -->
    <div
      class="relative z-10
             w-[calc(100%-2rem)] max-w-[400px]
             box-border overflow-hidden
             pixel-panel"
      @click.stop
    >
      <!-- 닫기 버튼(이미지) -->
      <button
        class="absolute top-4 right-4 z-20
               w-8 h-8 flex items-center justify-center"
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

      <!-- 내용 -->
      <div class="pixel-panel__content">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import quitIcon from '@/assets/icons/quit_icon.png'

const emit = defineEmits(['close'])
const emitClose = () => emit('close')
</script>