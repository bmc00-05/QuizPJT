<template>
  <div class="text-black p-4 space-y-4">
    <h2 class="text-lg font-bold">메뉴</h2>

    <p class="text-sm text-gray-700">
      로그아웃 하시겠습니까?
    </p>


    <div class="max-w-100 flex justify-center button-red">
      <button
        class="flex-1 text-lg font-bold"
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
