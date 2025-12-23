<template>
  <div class="w-full h-full min-h-0 flex flex-col text-black relative">
    <!-- ✅ GAME OVER 오버레이 -->
    <div
      v-if="isGameOver"
      class="absolute inset-0 z-[999] flex items-center justify-center bg-black/70"
    >
      <div class="pixel-panel max-w-[320px] w-[90%]">
        <div class="pixel-panel__content text-center py-6">
          <div class="text-2xl font-black tracking-widest text-red-200">
            GAME OVER
          </div>
          <div class="text-sm text-white/80 mt-2">
            맵으로 이동합니다...
          </div>
        </div>
      </div>
    </div>
    <!-- 🟢 퀴즈 진행 화면 -->
    <div v-if="!isFinished && currentQuestion" class="flex-1 min-h-0">
      <div class="relative rounded overflow-hidden flex flex-col h-full min-h-0">

        <!-- 문제 영역(고정) -->
        <div class="quiz-panel text-black shrink-0">
<div class="flex items-center justify-between px-2 py-1 text-xs">
  <span>{{ currentIndex + 1 }} / {{ totalProblems }}</span>

  <!-- ❤️ 하트 3개 -->
  <div class="flex items-center gap-1">
    <span
      v-for="i in 3"
      :key="i"
      class="text-base leading-none"
      :class="i <= hearts ? 'opacity-100' : 'opacity-20'"
    >
      ❤️
    </span>
  </div>
</div>

          <div v-if="result">
            <h3>결과: {{ result.correct }}</h3>
            <h3>정답: {{ result.correct_answer }}</h3>
            <h3>설명: {{ result.explanation }}</h3>
          </div>

          <div v-else class="flex items-center justify-center text-center min-h-[100px] px-3">
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

        <!-- ✅ 액션 패널 -->
        <div class="flex-1 min-h-0 overflow-hidden">
          <div class="pixel-panel h-full min-h-0">
            <div class="pixel-panel__content p-0 h-full min-h-0 overflow-hidden">
              <div class="relative h-full w-full overflow-hidden bg-black/5 rounded">
                <!-- ✅ 겹치는 레이어 -->
                <div class="absolute inset-0 pointer-events-none">
                    <div
                      v-if="hitFx"
                      class="absolute inset-0 z-30 bg-red-300/20"
                    ></div>
                  <!-- 플레이어 -->
                  <div class="absolute left-[30%] top-1/2 -translate-x-1/2 -translate-y-1/2 z-20">
                    <ActionSheet
                      :src="playerSheet"
                      :frameWidth="448"
                      :frameHeight="256"
                      :cols="10"
                      :row="anim.row"
                      :start="anim.start"
                      :frames="anim.frames"
                      :fps="anim.fps"
                      :loop="anim.loop"
                      :play="true"
                      :scale="0.9"
                      :offsetX="60"
                      :offsetY="0"
                      @finished="onAnimFinished"
                      class="block [image-rendering:pixelated]"
                    />
                  </div>

                  <!-- 적 -->
                  <div class="absolute right-[-20%] top-1/2 -translate-y-1/2 z-10">
                    <ActionSheet
                      v-if="enemyDef"
                      :src="enemyDef.sheet"
                      :frameWidth="enemyDef.frameWidth"
                      :frameHeight="enemyDef.frameHeight"
                      :cols="enemyDef.cols"
                      :row="enemyAnim.row"
                      :start="enemyAnim.start"
                      :frames="enemyAnim.frames"
                      :fps="enemyAnim.fps"
                      :loop="enemyAnim.loop"
                      :play="true"
                      :scale="enemyDef.scale"
                      :offsetX="enemyDef.offsetX ?? 0"
                      :offsetY="enemyDef.offsetY ?? 0"
                      :flipX="enemyDef.flipX ?? false"
                      @finished="onEnemyAnimFinished"
                      class="block [image-rendering:pixelated]"
                    />
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>

        <!-- 하단 버튼바 -->
        <div class="shrink-0 p-3 flex justify-end gap-2">
          <button
            v-if="!isAnswered"
            class="btn px-4 py-2 disabled:opacity-50"
            :disabled="selectedChoice === null || isChecking"
            @click="checkQuiz"
          >
            제출
          </button>

          <button v-else-if="!pendingFinish" class="btn px-4 py-2" @click="nextQuestion">
            다음 문제
          </button>

          <button v-else class="btn px-4 py-2 opacity-60 cursor-not-allowed" disabled>
            결과 정리중...
          </button>
        </div>

      </div>
    </div>

    <!-- 로딩 -->
    <div v-else-if="isLoadingSession" class="text-black">
      세션 준비 중...
    </div>

    <!-- 결과 모달 -->
    <BaseModal v-if="isFinished && sessionResult && modal.isOpen" @close="closeDetail">
      <h2 class="text-lg font-bold text-black">결과</h2>

      <p class="text-black">
        맞춘 문제: {{ sessionResult.correct }} / {{ sessionResult.total }}
      </p>
      <p class="text-black">획득 경험치: {{ sessionResult.score }}</p>
      <p class="text-black">
        레벨: {{ sessionResult.level_before }} → {{ sessionResult.level_after }}
      </p>

      <button class="mt-4 w-full bg-gray-800 text-white py-2 rounded" @click="closeDetail">
        닫기
      </button>
    </BaseModal>
  </div>

  <BaseModal v-if="leaveOpen" @close="cancelLeave">
    <LeaveConfirm @confirm="confirmLeave" @cancel="cancelLeave" />
  </BaseModal>

</template>

<script setup>
import ActionSheet from "@/components/ActionSheet.vue"
import { reactive, ref, onMounted, onBeforeUnmount, computed, watch } from "vue"
import { useAccountStore } from "@/stores/accounts"
import { useUserStore } from "@/stores/user"
import { useRoute, useRouter, onBeforeRouteLeave } from "vue-router"
import axios from "axios"
import BaseModal from "@/components/common/BaseModal.vue"
import { useModalStore } from "@/stores/modal"
import LeaveConfirm from "@/components/LeaveConfirm.vue"
import playerSheet from "@/assets/character/main_cat.png"
import { ANIMS, PICK_RULES } from "@/game/anims"
import { ENEMIES } from "@/game/enemies"

const modal = useModalStore()
const router = useRouter()
const route = useRoute()

const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()
const userStore = useUserStore()

const problemSetId = computed(() => route.params.id ?? route.params.problemSetId)

// -----------------------------
// 퀴즈/세션 상태
// -----------------------------
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

const hearts = ref(3)

// ✅ GAME OVER 상태
const isGameOver = ref(false)
let gameOverTimer = null
const GAME_OVER_DELAY_MS = 2000


const triggerGameOver = () => {
  if (isGameOver.value) return
  isGameOver.value = true

  // 혹시 남아있는 종료 대기 로직 있으면 무효화
  pendingFinish.value = false
  pendingFinishResult.value = null
  pendingAfterOnceKey.value = null
  enemyAfterOnceKey.value = null

  // 모달 열려있으면 닫기(있을 수도 있어서 방어)
  modal.close?.()

  // 잠깐 보여주고 맵으로 이동
  gameOverTimer = setTimeout(() => {
    router.replace({ name: "map" })  // ✅ 너 라우터 name이 map 맞으면 그대로
  }, GAME_OVER_DELAY_MS)
}

onBeforeUnmount(() => {
  if (gameOverTimer) clearTimeout(gameOverTimer)
})


// ----------------------------
// 이탈 경고
// ----------------------------
// ✅ 라우팅 이탈 경고 모달 상태
const leaveOpen = ref(false)
const pendingTo = ref(null)
const allowLeaveOnce = ref(false)

// ✅ 게임 진행 중일 때만 막기(원하는 조건으로 조절 가능)
const shouldBlockLeave = computed(() => {
  // 세션 생성됐고, 아직 끝/게임오버 아니면 “진행 중”
  return !!sessionId.value && !isFinished.value && !isGameOver.value
})

// ✅ 라우팅 가드: 나가려는 순간 잡기(네비바/뒤로가기 포함)
onBeforeRouteLeave((to, from, next) => {
  // ✅ 사용자가 "나가기"를 눌러서 허용된 1회 이동이면 통과
  if (allowLeaveOnce.value) {
    allowLeaveOnce.value = false
    return next()
  }

  if (!shouldBlockLeave.value) return next()

  if (leaveOpen.value) return next(false)

  pendingTo.value = to
  leaveOpen.value = true
  next(false)
})

const confirmLeave = async () => {
  leaveOpen.value = false
  pendingTo.value = null
  allowLeaveOnce.value = true
  await router.replace({ name: "map" })
}

const cancelLeave = () => {
  leaveOpen.value = false
  pendingTo.value = null
}

const onBeforeUnload = (e) => {
  if (!shouldBlockLeave.value) return
  e.preventDefault()
  e.returnValue = "" // 크롬/사파리/엣지: 문구는 무시되고 기본 경고 뜸
}

onMounted(() => {
  window.addEventListener("beforeunload", onBeforeUnload)
})

onBeforeUnmount(() => {
  window.removeEventListener("beforeunload", onBeforeUnload)
})
// -----------------------------
// 마지막 문제: 애니 끝난 뒤 모달
// -----------------------------
const pendingFinish = ref(false)
const pendingFinishResult = ref(null)

function commitFinish(session_result) {
  isFinished.value = true
  sessionResult.value = session_result
  userStore.applySessionResult(session_result)
  modal.open(1)
}

function tryCommitFinish() {
  if (!pendingFinish.value || !pendingFinishResult.value) return
  if (pendingAfterOnceKey.value) return
  if (enemyAfterOnceKey.value) return

  const finalResult = pendingFinishResult.value
  pendingFinish.value = false
  pendingFinishResult.value = null
  commitFinish(finalResult)
}

// -----------------------------
// 플레이어 애니
// -----------------------------
const anim = reactive({ ...ANIMS.idle_0 })
const pendingAfterOnceKey = ref(null)
const currentIdleKey = ref("idle_0")

function applyAnim(key) {
  const clip = ANIMS[key]
  if (!clip) return
  anim.row = clip.row
  anim.start = clip.start
  anim.frames = clip.frames
  anim.fps = clip.fps
  anim.loop = clip.loop
}

function playOnce(onceKey, afterKey) {
  const clip = ANIMS[onceKey]
  if (!clip) return
  applyAnim(onceKey)

  // ✅ 혹시라도 loop=true가 들어오면 finish가 안 떠서 막히니까 방어
  if (clip.loop) {
    applyAnim(afterKey)
    pendingAfterOnceKey.value = null
  } else {
    pendingAfterOnceKey.value = afterKey
  }
}

// ✅ 피격 이펙트(흔들림/플래시)
const hitFx = ref(false)
let hitFxTimer = null

const triggerHitFx = () => {
  hitFx.value = true
  if (hitFxTimer) clearTimeout(hitFxTimer)
  hitFxTimer = setTimeout(() => (hitFx.value = false), 220)
}

onBeforeUnmount(() => {
  if (hitFxTimer) clearTimeout(hitFxTimer)
})

// ✅ 유저 피격 애니(있으면 재생, 없으면 이펙트만)
const playPlayerHit = () => {
  triggerHitFx()
  if (ANIMS?.hurt) {
    // 피격 한 번 -> 원래 idle로 복귀
    playOnce("hurt", currentIdleKey.value || "idle_0")
  }
}

// -----------------------------
// 적(Enemy) 애니
// -----------------------------
const enemyId = ref("slime")
const enemyDef = computed(() => ENEMIES[enemyId.value])

const enemyAnim = reactive({ row: 0, start: 0, frames: 1, fps: 8, loop: true })
const enemyAfterOnceKey = ref(null)

function applyEnemy(key) {
  const def = enemyDef.value
  if (!def?.anims) return
  const clip = def.anims[key]
  if (!clip) return
  enemyAnim.row = clip.row
  enemyAnim.start = clip.start
  enemyAnim.frames = clip.frames
  enemyAnim.fps = clip.fps
  enemyAnim.loop = clip.loop
}

function playOnceEnemy(onceKey, afterKey) {
  const def = enemyDef.value
  const clip = def?.anims?.[onceKey]
  if (!clip) return

  applyEnemy(onceKey)

  if (clip.loop) {
    applyEnemy(afterKey)
    enemyAfterOnceKey.value = null
  } else {
    enemyAfterOnceKey.value = afterKey
  }
}

watch(
  enemyDef,
  (def) => {
    if (!def?.anims?.idle) return
    enemyAfterOnceKey.value = null
    applyEnemy("idle")
  },
  { immediate: true }
)

// -----------------------------
// finished 핸들러
// -----------------------------
function onAnimFinished() {
  if (pendingAfterOnceKey.value) {
    applyAnim(pendingAfterOnceKey.value)
    pendingAfterOnceKey.value = null
  }
  tryCommitFinish()
}

function onEnemyAnimFinished() {
  if (enemyAfterOnceKey.value) {
    applyEnemy(enemyAfterOnceKey.value)
    enemyAfterOnceKey.value = null
  }
  tryCommitFinish()
}

// -----------------------------
// UI 이벤트
// -----------------------------
function onPick(n) {
  if (isGameOver.value) return
  if (isAnswered.value) return
  selectedChoice.value = n

  const rule = PICK_RULES[n]
  if (!rule) return

  currentIdleKey.value = rule.idle ?? "idle_0"

  if (rule.switchOnce) playOnce(rule.switchOnce, currentIdleKey.value)
  else applyAnim(currentIdleKey.value)
}

const nextQuestion = () => {
  if (isGameOver.value) return
  result.value = null
  isAnswered.value = false
  selectedChoice.value = null

  pendingFinish.value = false
  pendingFinishResult.value = null

  pendingAfterOnceKey.value = null
  currentIdleKey.value = "idle_0"
  applyAnim("idle_0")

  enemyAfterOnceKey.value = null
  applyEnemy("idle")

  if (currentIndex.value + 1 >= quizList.value.length) return
  currentIndex.value++
}

// -----------------------------
// API
// -----------------------------
const createSession = async () => {
  hearts.value = 3
  isGameOver.value = false
  
  if (!problemSetId.value) {
    alert("문제집 id가 없습니다.")
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
    totalProblems.value = res.data.total_problems ?? quizList.value.length

    if (quizList.value.length === 0) {
      alert("이 문제집에는 문제가 없습니다. 문제를 추가한 뒤 시작할 수 있어요.")
      router.back()
      return
    }
  } catch (err) {
    console.error(err)
    alert("게임을 시작할 수 없습니다. (문제집에 문제가 없거나 서버 오류)")
    router.back()
  } finally {
    isLoadingSession.value = false
  }
}

const checkQuiz = async () => {
  if (isGameOver.value) return
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

  // ✅ 정답일 때: 플레이어 공격 + 적 hit
  if (res.data.correct === true) {
    const rule = PICK_RULES[selectedChoice.value]
    if (rule?.attackOnce) playOnce(rule.attackOnce, currentIdleKey.value || rule.idle || "idle_0")
    if (enemyDef.value?.anims?.hit) playOnceEnemy("hit", "idle")
  }

  // ✅ 오답일 때: 적 공격 + 하트 감소
  if (res.data.correct === false) {
    // 적 공격(없으면 생략)
    if (enemyDef.value?.anims?.attack) {
      playOnceEnemy("attack", "idle")
    }

    // ✅ 유저 피격(애니 + 이펙트)
    playPlayerHit()

    hearts.value = Math.max(0, hearts.value - 1)

    // ✅ 하트 0이면 즉시 맵으로 이동
    if (hearts.value <= 0) {
      triggerGameOver()   // ✅ 오버레이 띄우고, 2초 뒤 이동
      return
    }
  }

  // ✅ 마지막 문제면: (단, 하트 0으로 종료되기 전에만) 둘 다 끝난 뒤 모달
  if (res.data.is_completed) {
    pendingFinish.value = true
    pendingFinishResult.value = res.data.session_result
    tryCommitFinish()
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

onMounted(createSession)
</script>

<style scoped>
@keyframes hitShake {
  0% { transform: translate(-50%, -50%) translateX(0); }
  25% { transform: translate(-50%, -50%) translateX(-6px); }
  50% { transform: translate(-50%, -50%) translateX(6px); }
  75% { transform: translate(-50%, -50%) translateX(-4px); }
  100% { transform: translate(-50%, -50%) translateX(0); }
}

/* 플레이어 컨테이너가 이미 -translate-x/y로 중앙정렬중이라
  transform이 덮이지 않게 "컨테이너에 class"를 주는 대신
   위처럼 동일한 기준 transform을 유지하는 방식 */
.hit-shake {
  animation: hitShake 0.22s ease-in-out;
}

</style>
