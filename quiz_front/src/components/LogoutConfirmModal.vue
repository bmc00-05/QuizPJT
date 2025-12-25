<template>
  <div class="text-black p-4 space-y-4">
    <h2 class="text-lg font-bold">메뉴</h2>

    <p class="text-sm text-gray-700">
      로그아웃 하시겠습니까?
    </p>

    <div class="max-w-100 red-button">
      <button
        class="flex-1 pixel-panel__content"
        @click="emit('logout')"
      >
        로그아웃
      </button>

    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['close', 'logout'])
</script>
