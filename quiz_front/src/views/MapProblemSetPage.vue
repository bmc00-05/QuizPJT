<template>
  <div>
    <h1>맵 문제집 목록</h1>
    <ul>
      <li v-for="problemSet in problemSets.problem_sets" :key="problemSet.id" class="cursor-pointer hover:underline"
        @click="openDetail(problemSet)">
        {{ problemSet.title}}
        
      </li>
    </ul>
      <ProblemSetDetail
    v-if="selectedProblemSet"
    :open="isModalOpen"
    :problem-set="selectedProblemSet"
    @close="closeDetail"
  />
  </div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { useRoute } from 'vue-router'
import axios from 'axios'
import ProblemSetDetail from '@/components/ProblemSetDetail.vue'

const accountStore = useAccountStore()
const route = useRoute()

const problemSetId = ref(route.params.problemset)

const problemSets = ref([])

const selectedProblemSet = ref(null)
const isModalOpen = ref(false)

const openDetail = (data) => {
  selectedProblemSet.value = data
  isModalOpen.value = true
}

const closeDetail = () => {
  isModalOpen.value = false
  selectedProblemSet.value = null
}

const getProblemSets = async () => {
  try {
    
    const res = await axios.get(
      `http://127.0.0.1:8000/api/v1/game/maps/${problemSetId.value}`,
      {
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      }
    )

    problemSets.value = res.data

  } catch (err) {
    console.error(err)
  }
}

onMounted(() => {
  getProblemSets()
})
</script>

<style scoped>

</style>