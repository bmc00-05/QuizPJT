<template>
  <div>
    <h1>유저 모드 페이지</h1>
  </div>
    <ul>
      <li v-for="quizset in quizsets" :key="quizset.id">
        <RouterLink :to="{ name: 'mainproblemset', params: {'problemset':map.id}}">
        {{ map.name }} - {{ map.description }}
        </RouterLink>
      </li>
    </ul>
  <div>
    <RouterLink :to="{ name: 'createQuizSet'}"> 문제집 생성 </RouterLink>
  </div>
</template>

<script setup>

</script>

<style scoped>

</style>