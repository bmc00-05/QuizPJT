<template>
  <div class="w-full h-full min-h-0 flex flex-col text-black">
    <!-- 🟢 퀴즈 진행 화면 -->
<div v-if="!isFinished && currentQuestion" class="flex-1 min-h-0">
  <!-- ✅ 전체를 세로 flex로 -->
  <div class="relative rounded overflow-hidden flex flex-col h-full min-h-0">

    <!-- 문제 영역(고정) -->
    <div class="quiz-panel text-black shrink-0">
      <p class="flex text-black text-xs justify-center">
        {{ currentIndex + 1 }} / {{ totalProblems }}
      </p>

      <div v-if="result">
        <h3>결과: {{ result.correct }}</h3>
        <h3>정답: {{ result.correct_answer }}</h3>
        <h3>설명: {{ result.explanation }}</h3>
      </div>

      <div
        v-else
        class="flex items-center justify-center text-center min-h-[100px] px-3"
      >
        {{ currentQuestion.question }}
      </div>
    </div>

    <!-- 보기 2x2(고정) -->
    <div class="text-black shrink-0">
      <ul class="grid grid-cols-2">
        <li
          v-for="n in 4"
          :key="n"
          class="flex items-center justify-center quiz-panel"
          @click="onPick(n)"
          :class="[
            isAnswered ? 'opacity-60 pointer-events-none' : '',
            selectedChoice === n ? 'ring-2 ring-amber-50' : ''
          ]"
        >
          <div class="pixel-panel__content text-black text-sm flex items-center justify-center text-center min-h-[64px]">
            {{ currentQuestion[`choice${n}`] }}
          </div>
        </li>
      </ul>
    </div>

    <!-- ✅ 액션 패널(남은 공간 최대 차지) -->
<div class="flex-1 min-h-0 overflow-hidden">
  <div class="pixel-panel h-full min-h-0">
    <!-- 🔥 overflow-auto 제거(스크롤 생기면 중앙정렬 깨짐) -->
    <div class="pixel-panel__content h-full min-h-0 overflow-hidden">

      <!-- ✅ 스프라이트 영역: 반드시 h-full -->
      <div class="relative h-full w-full overflow-hidden bg-black/5 rounded">
        <div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
          <ActionSheet
            :src="idleSheet"
            :frameWidth="256"
            :frameHeight="256"
            :cols="10"
            :row="anim.row"
            :start="anim.start"
            :frames="anim.frames"
            :fps="anim.fps"
            :loop="anim.loop"
            :play="true"
            :scale="1"
            @finished="onAnimFinished"
            class="block [image-rendering:pixelated]"
          />
        </div>
      </div>

    </div>
  </div>
</div>

    <!-- ✅ 하단 버튼바(제일 아래 + 오른쪽) -->
    <div class="shrink-0 p-3 flex justify-end gap-2">
      <button
        v-if="!isAnswered"
        class="btn px-4 py-2 disabled:opacity-50"
        :disabled="selectedChoice === null || isChecking"
        @click="checkQuiz"
      >
        제출
      </button>

      <button
        v-else
        class="btn px-4 py-2"
        @click="nextQuestion"
      >
        다음 문제
      </button>
    </div>

  </div>
</div>


    <!-- ✅ 로딩 -->
    <div v-else-if="isLoadingSession" class="text-black">
      세션 준비 중...
    </div>

    <!-- ✅ 결과 모달: 바깥에 둬야 isFinished=true에서도 렌더됨 -->
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
  </div>
</template>


<script setup>
import ActionSheet from "@/components/ActionSheet.vue";
import { reactive, ref, onMounted, computed } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { useUserStore } from '@/stores/user'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import BaseModal from '@/components/common/BaseModal.vue'
import { useModalStore } from '@/stores/modal'
import idleSheet from "@/assets/character/pose_idle.png";
import { ANIMS, PICK_RULES } from "@/game/anims"


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

  pendingLoopKey.value = null
  applyAnim("idle_0")

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


//  애니메이션


// ✅ 현재 스프라이트 애니메이션 상태(클립)
// 첫 진입은 idle_0
const anim = reactive({ ...ANIMS.idle_0 })

// ✅ switch(1회) 끝난 뒤 넘어갈 loop 애니메이션 key를 저장
const pendingLoopKey = ref(null)

/**
 * ✅ ANIMS 테이블의 key로 anim 상태를 교체 적용하는 함수
 * - reactive 객체를 "교체"하는 게 아니라 "값을 덮어쓰기" 해야 반응성이 유지됨
 */
function applyAnim(key) {
  const clip = ANIMS[key]
  if (!clip) return
  anim.row = clip.row
  anim.start = clip.start
  anim.frames = clip.frames
  anim.fps = clip.fps
  anim.loop = clip.loop
}

/**
 * ✅ 보기 클릭 시 처리
 * - 선택지 저장
 * - 1,2번이면: switch 1회 재생 후 → idle 루프로 전환 예약
 * - 3,4번은 일단은 아무 것도 안함(원하면 규칙 추가 가능)
 */
function onPick(n) {
  if (isAnswered.value) return

  selectedChoice.value = n

  // 1~2번만 애니메이션 전환 (원하면 3,4도 규칙 추가)
  const rule = PICK_RULES[n]
  if (!rule) return

  // 1) switch 애니메이션 1회 재생
  applyAnim(rule.once)

  // 2) switch 끝나면 loop로 바꿀 수 있게 "예약"
  pendingLoopKey.value = rule.loop
}

/**
 * ✅ SpriteSheet에서 loop=false 애니메이션이 끝나면 호출됨
 * - 예약된 loopKey가 있으면 그 idle로 전환
 */
function onAnimFinished() {
  if (!pendingLoopKey.value) return
  applyAnim(pendingLoopKey.value)
  pendingLoopKey.value = null
}
</script>

<style scoped>
</style>
