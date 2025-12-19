<template>
  <h1>게임화면</h1>
  <!-- 🟢 퀴즈 진행 화면 -->
  <div v-if="!isFinished && currentQuestion">
    <h4>현재 진행: {{ currentIndex +1 }}</h4>
    <h4>현재 선택: {{ selectedChoice }}</h4>
    <div>
      <h2>문제: {{ currentQuestion.question }}</h2>
    </div>
    <ul>
      <li v-for="n in 4" :key="n" @click="selectedChoice = n">
        {{ currentQuestion[`choice${n}`] }}
      </li>
    </ul>
    <hr/>
    
    <div v-if="result">
      <h3>결과: {{ result.correct }}</h3>
      <h3>정답: {{ result.correct_answer }}</h3>
      <h3>설명: {{ result.explanation }}</h3>
    </div>
  <button
    v-if="!isAnswered"
    :disabled="selectedChoice === null || isChecking"
    @click="checkQuiz"
  >
    채점
  </button>

  <button
    v-else-if="!isFinished"
    @click="nextQuestion"
  >
    다음 문제
  </button>
  </div>

<!-- 🟡 결과창 -->
<div v-if="isFinished && sessionResult">
  <h2>결과</h2>
  <p>맞춘 문제: {{ sessionResult.correct }} / {{ sessionResult.total }}</p>
  <p>획득 경험치: {{ sessionResult.score }}</p>
  <p>레벨: {{ sessionResult.level_before }} → {{ sessionResult.level_after }}</p>
</div>
<div>
  {{ sessionResult }}
</div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { useUserStore } from '@/stores/user'
import { useRoute } from 'vue-router'
import axios from 'axios'

// 
const route = useRoute()
const accountStore = useAccountStore()
const userStore = useUserStore()

const problemSetId = route.params.problemSetId

const sessionId = ref(null)
const quizList = ref([])
const currentIndex = ref(0)
const selectedChoice = ref(null)
const result = ref(null)
const isChecking = ref(false)

const isAnswered = ref(false)
const isFinished = ref(false)
const sessionResult = ref(null)

const currentQuestion = computed(() => {
  return quizList.value[currentIndex.value]
})

const nextQuestion = () => {
  result.value = null
  isAnswered.value = false 
  selectedChoice.value = null
  currentIndex.value++
}


const createSession = async () => {
  try {
    
    const res = await axios.post(
      'http://127.0.0.1:8000/api/v1/game/quiz/play/',
      {
        problem_set_id: problemSetId
      },
      {
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      }
    )

    sessionId.value = res.data.session_id
    quizList.value = res.data.problems

  } catch (err) {
    console.error(err)
  }
}

const checkQuiz = async () => {

  if (
    !sessionId.value ||
    !currentQuestion.value ||
    selectedChoice.value === null
  ) return

  try {
    isChecking.value = true

    const res = await axios.post(
      'http://127.0.0.1:8000/api/v1/game/quiz/check/',
      {
        session_id: sessionId.value,
        question_id: currentQuestion.value.id,
        selected: selectedChoice.value
      },
      {
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      }
    )
    
    result.value = res.data
    isAnswered.value = true

    if (res.data.is_completed) {
      console.log("세션완성")
      isFinished.value = true
      sessionResult.value = res.data.session_result
      // pinia 갱신
      userStore.applySessionResult(res.data.session_result)
    }

  } catch (err) {
    console.error(err)
  } finally {
    isChecking.value = false 
  }
}


onMounted(() => {
  createSession()
})
</script>

<style scoped>

</style>