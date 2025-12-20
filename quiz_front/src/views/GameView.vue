<template>
  <h1>게임화면</h1>

  <!-- 🟢 퀴즈 진행 화면 -->
  <div v-if="!isFinished && currentQuestion">
    <h4>현재 진행: {{ currentIndex + 1 }} / {{ totalProblems }}</h4>
    <h4>현재 선택: {{ selectedChoice }}</h4>

    <div>
      <h2>문제: {{ currentQuestion.question }}</h2>
    </div>

    <ul>
      <li
        v-for="n in 4"
        :key="n"
        class="cursor-pointer"
        @click="!isAnswered && (selectedChoice = n)"
        :style="isAnswered ? 'opacity:0.6; pointer-events:none;' : ''"
      >
        {{ currentQuestion[`choice${n}`] }}
      </li>
    </ul>

    <hr />

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

    <button v-else-if="!isFinished" @click="nextQuestion">
      다음 문제
    </button>
  </div>

  <!-- ✅ 로딩/에러 상태(선택) -->
  <div v-else-if="isLoadingSession" class="text-black">
    세션 준비 중...
  </div>

  <!-- 🟡 결과 모달 -->
  <BaseModal
    v-if="isFinished && sessionResult && modal.isOpen"
    @close="closeDetail"
  >
    <h2 class="text-lg font-bold text-black">결과</h2>

    <p class="text-black">
      맞춘 문제: {{ sessionResult.correct }} / {{ sessionResult.total }}
    </p>
    <p class="text-black">획득 경험치: {{ sessionResult.score }}</p>
    <p class="text-black">
      레벨: {{ sessionResult.level_before }} → {{ sessionResult.level_after }}
    </p>

    <button
      class="mt-4 w-full bg-gray-800 text-white py-2 rounded"
      @click="closeDetail"
    >
      닫기
    </button>
  </BaseModal>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { useUserStore } from '@/stores/user'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import BaseModal from '@/components/common/BaseModal.vue'
import { useModalStore } from '@/stores/modal'

const modal = useModalStore()
const router = useRouter()
const route = useRoute()

const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()
const userStore = useUserStore()

// ✅ 라우트 파라미터 안전 처리 (id or problemSetId)
const problemSetId = computed(() => route.params.id ?? route.params.problemSetId)

const sessionId = ref(null)
const quizList = ref([])
const totalProblems = ref(0)

const currentIndex = ref(0)
const selectedChoice = ref(null)
const result = ref(null)
const isChecking = ref(false)

const isAnswered = ref(false)
const isFinished = ref(false)
const sessionResult = ref(null)

const isLoadingSession = ref(false)

const currentQuestion = computed(() => quizList.value[currentIndex.value])

const nextQuestion = () => {
  result.value = null
  isAnswered.value = false
  selectedChoice.value = null

  // ✅ 범위 보호 (혹시 서버 완료 플래그가 늦거나 누락되어도 안전)
  if (currentIndex.value + 1 >= quizList.value.length) {
    // 여기서는 그냥 막기만(완료 처리는 서버가 is_completed로 하니까)
    return
  }

  currentIndex.value++
}

const createSession = async () => {
  if (!problemSetId.value) {
    alert('문제집 id가 없습니다.')
    router.back()
    return
  }

  isLoadingSession.value = true

  try {
    const res = await axios.post(
      `${API_URL}/game/quiz/play/`,
      { problem_set_id: Number(problemSetId.value) },
      { headers: { Authorization: `Token ${accountStore.token}` } }
    )

    sessionId.value = res.data.session_id
    quizList.value = res.data.problems || []

    // ✅ 서버가 total_problems 내려주면 그걸 사용, 없으면 배열 길이로 대체
    totalProblems.value = res.data.total_problems ?? quizList.value.length

    // ✅ 0개면 바로 차단
    if (quizList.value.length === 0) {
      alert('이 문제집에는 문제가 없습니다. 문제를 추가한 뒤 시작할 수 있어요.')
      router.back()
      return
    }
  } catch (err) {
    console.error(err)
    alert('게임을 시작할 수 없습니다. (문제집에 문제가 없거나 서버 오류)')
    router.back()
  } finally {
    isLoadingSession.value = false
  }
}

const checkQuiz = async () => {
  if (!sessionId.value || !currentQuestion.value || selectedChoice.value === null) return

  try {
    isChecking.value = true

    const res = await axios.post(
      `${API_URL}/game/quiz/check/`,
      {
        session_id: sessionId.value,
        question_id: currentQuestion.value.id,
        selected: selectedChoice.value,
      },
      { headers: { Authorization: `Token ${accountStore.token}` } }
    )

    result.value = res.data
    isAnswered.value = true

    if (res.data.is_completed) {
      isFinished.value = true
      sessionResult.value = res.data.session_result

      // pinia 갱신
      userStore.applySessionResult(res.data.session_result)
      modal.open(1)
    }
  } catch (err) {
    console.error(err)
  } finally {
    isChecking.value = false
  }
}

const closeDetail = () => {
  modal.close()
  router.back()
}

onMounted(() => {
  createSession()
})
</script>

<style scoped>
</style>
