<template>
  <div class="overlay">
    <div class="relative justify-center w-full max-w-sm rounded-2xl bg-white p-6 shadow-xl">
      <p>제목[난이도]: {{ data.problemSet.title }}</p>
      <p>설명: {{ data.problemSet.description }}</p>
      <p>좋아요: {{ data.problemSet.like_count }}</p>
      <p>작성자: {{ data.problemSet.created_by_name }}</p>
      <button @click="$emit('close')" class="absolute right-4 top-4 text-gray-400 hover:text-gray-600"
        aria-label="Close">✕</button>
      <div class="mt-5">
        <RouterLink class="btn":to="{ name: 'game', params: { problemSetId: data.problemSet.id }}">시작</RouterLink>
      </div>
      
    </div>
  </div>
</template>

<script setup>
const data = defineProps({
  problemSet: Object
})
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.box {
  background: white;
  padding: 20px;
}
</style>