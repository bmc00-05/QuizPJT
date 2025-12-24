<template>
  <div class="w-full text-black max-w-[360px] mx-auto">
    <div class="text-xl font-black text-center mb-2">잠깐!</div>
    <div class="text-sm text-black/70 text-center">
      지금 나가면 진행 중인 퀴즈가 종료돼요.<br />
      정말 나갈까요?
    </div>

    <div class="mt-4 flex gap-2">
      <button class="flex-1 btn px-4 py-2" @click="$emit('confirm')">
        나가기
      </button>
      <button
        class="flex-1 px-4 py-2 rounded border bg-white/70 hover:bg-white"
        @click="$emit('cancel')"
      >
        계속하기
      </button>
    </div>
  </div>
</template>

<script setup>
defineEmits(["confirm", "cancel"])
</script>