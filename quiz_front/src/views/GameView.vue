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
<!-- 문제 영역(고정) -->
<div class="quiz-panel text-black shrink-0 flex flex-col h-[140px] min-h-[140px] max-h-[140px] overflow-hidden">
  <!-- ✅ 채점 결과: 해설 -> 정답 (위아래) + 중앙정렬 -->
  <div
    v-if="result"
    class="h-full px-3 py-3 flex flex-col items-center justify-center text-center gap-2 min-h-0"
  >
    <!-- 해설이 길면 여기만 스크롤 -->
    <div class="text-sm text-black/90 w-full max-h-[72px] overflow-y-auto">
      {{ result.explanation }}
    </div>

    <div class="text-sm font-black shrink-0">
      정답: {{ result.correct_answer }}
    </div>
  </div>

  <!-- ✅ 문제 표시: 패널 제일 하단 중앙 -->
  <div v-else class="h-full px-3 py-3 flex flex-col items-center justify-center min-h-0">
    <div class="w-full max-h-[96px] overflow-y-auto text-center">
      {{ currentQuestion.question }}
    </div>
  </div>
</div>

<!-- 보기 2x2(고정) -->
<div class="text-black shrink-0">
  <ul class="grid grid-cols-2 grid-rows-2 h-[176px]">
    <li
      v-for="n in 4"
      :key="n"
      class="flex items-center justify-center quiz-panel h-full"
      @click="onPick(n)"
      :class="[
        isAnswered ? 'opacity-60 pointer-events-none' : '',
        selectedChoice === n ? 'ring-2 ring-amber-50' : ''
      ]"
    >
      <div class="pixel-panel__content text-black text-sm flex items-center justify-center text-center h-full w-full p-2">
        <!-- 선택지 텍스트는 2줄까지만 보이게(아래 style 추가) -->
        <span class="clamp-2 break-words leading-tight">
          {{ currentQuestion[`choice${n}`] }}
        </span>
      </div>
    </li>
  </ul>
</div>

        <!-- ✅ 액션 패널 -->
        <div class="flex-1 min-h-0 overflow-hidden">
          <div class="pixel-panel h-full min-h-0">
            <div class="pixel-panel__content p-0 h-full min-h-0 overflow-hidden">
              <div class="relative h-full w-full overflow-hidden bg-black/5 rounded">


  <!-- ✅ HUD: 상단 중앙 라운드 + 하트 -->
  <div class="absolute top-2 left-1/2 -translate-x-1/2 z-40 flex flex-col items-center gap-1 pointer-events-none">
    <div class="text-xs px-2 py-1 rounded bg-black/40 text-white">
      {{ currentIndex + 1 }} / {{ totalProblems }}
    </div>

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

                <!-- ✅ 겹치는 레이어 -->
                <div class="absolute inset-0 pointer-events-none">
                  ...
                </div>


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
<div
  v-if="enemyDef && enemyVisible"
  class="absolute top-1/2 z-10 transition-[left] ease-out will-change-[left]"
  :style="{
    left: `${enemyLeftPct}%`,
    transitionDuration: `${enemyTransitionMs}ms`,
  }"
>
  <div class="-translate-x-1/2 -translate-y-1/2">
    <ActionSheet
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
import { reactive, ref, onMounted, onBeforeUnmount, computed, watch, nextTick } from "vue"
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
  if (enemyBusy.value) return

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
// 적(Enemy) : 맵별 스폰 + hit→death→respawn
// -----------------------------
const spawnOnNext = ref(false) // ✅ 다음 문제로 넘어갈 때 적 스폰

const mapId = computed(() => {
  const ps = Number(problemSetId.value)
  if (!Number.isFinite(ps) || ps <= 0) return 1
  return Math.min(5, Math.max(1, Math.ceil(ps / 3))) // 1~3=1, 4~6=2, ...
})

const raf = () => new Promise((r) => requestAnimationFrame(r))
const enemyTransitionMs = ref(0) // ✅ 첫 프레임 0ms로 순간이동 후, 다음 프레임에 ENEMY_ENTER_MS로 변경

const MAP_ENEMY_POOLS = {
  1: ["slime", "skeleton", "skeleton_archer"],
  2: ["orc", "armored_orc", "axeman"],
  3: ["armored_skeleton", "greatsword_skeleton", "knight"],
  4: ["lancer", "swordman", "soldier"],
  5: ["elite_orc", "orc_rider", "werewolf", "werebear"],
}

const enemyPool = computed(() => MAP_ENEMY_POOLS[mapId.value] ?? ["slime"])

// ✅ 현재 적
const enemyId = ref(null)
const enemyDef = computed(() => (enemyId.value ? ENEMIES[enemyId.value] : null))

// ✅ 렌더/상태
const enemyVisible = ref(true)
const enemyBusy = ref(false)              // hit/death 등 “한 번 재생” 중
const enemyChain = ref(null)              // 'hit_then_death' | 'death_then_respawn' | null
const enemyLastOnce = ref(null)
const lastEnemyId = ref(null)

// ✅ enemy anim state
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

function playOnceEnemy(onceKey, afterKey = null) {
  const def = enemyDef.value
  const clip = def?.anims?.[onceKey]
  if (!clip) return

  enemyBusy.value = true
  enemyLastOnce.value = onceKey
  applyEnemy(onceKey)

  if (clip.loop) {
    if (afterKey) applyEnemy(afterKey)
    enemyAfterOnceKey.value = null
    enemyBusy.value = false
  } else {
    enemyAfterOnceKey.value = afterKey // null 가능
  }
}

const spawnEnemy = () => {
  const pool = enemyPool.value
  if (!pool?.length) return

  enemyVisible.value = false

  setTimeout(async () => {
    let next = pool[Math.floor(Math.random() * pool.length)]
    if (pool.length > 1 && next === lastEnemyId.value) {
      const idx = pool.indexOf(next)
      next = pool[(idx + 1) % pool.length]
    }

    lastEnemyId.value = next

    // ✅ "보이기 전에" 시작 위치 + transition 0
    enemyTransitionMs.value = 0
    enemyLeftPct.value = ENEMY_START_LEFT

    enemyId.value = next
    enemyVisible.value = true

    await nextTick()
    startEnemyEnter()
  }, 120)
}

// ✅ 정답 시: hit→death→respawn
const defeatEnemy = () => {
  const def = enemyDef.value
  if (!def) return
  if (enemyBusy.value) return

  const hasHit = !!def.anims?.hit
  const hasDeath = !!def.anims?.death

  if (hasHit && hasDeath) {
    enemyChain.value = "hit_then_death"
    playOnceEnemy("hit")
    return
  }
  if (hasDeath) {
    enemyChain.value = "death_then_respawn"
    playOnceEnemy("death")
    return
  }

   // ✅ fallback: 즉시 숨기고 다음 문제에서 스폰
  enemyVisible.value = false
  enemyBusy.value = false
  enemyChain.value = null

  if (!pendingFinish.value) spawnOnNext.value = true
  tryCommitFinish()
}

const ENEMY_START_LEFT = 130   // 화면 오른쪽 밖(%) 110~130 사이로 조절
const ENEMY_TARGET_LEFT = 78   // 최종 도착 위치(%) 65~80 사이로 조절
const enemyLeftPct = ref(ENEMY_START_LEFT)

// ✅ 적 등장(패널 밖 -> 안) 이동 연출
const enemyEnterOffset = ref(false)        // true면 바깥(오른쪽)으로 밀려있음
const enemyEnterInProgress = ref(false)
const ENEMY_ENTER_MS = 1100
let enemyEnterTimer = null

const startEnemyEnter = async () => {
  const def = enemyDef.value
  if (!def) return

  enemyEnterInProgress.value = true

  // 1) transition 끄고 시작 위치로 순간이동
  enemyTransitionMs.value = 0
  enemyLeftPct.value = ENEMY_START_LEFT

  await nextTick()
  await raf() // ✅ 여기서 "시작 위치"가 실제로 한 프레임 그려짐(페인트)

  // 2) 걷기 애니
  if (def.anims?.walk) applyEnemy("walk")
  else if (def.anims?.idle) applyEnemy("idle")

  // 3) 이제 transition 켜고 목표 위치로 이동
  enemyTransitionMs.value = ENEMY_ENTER_MS
  enemyLeftPct.value = ENEMY_TARGET_LEFT

  if (enemyEnterTimer) clearTimeout(enemyEnterTimer)
  enemyEnterTimer = setTimeout(() => {
    enemyEnterInProgress.value = false
    if (enemyDef.value?.anims?.idle) applyEnemy("idle")
  }, ENEMY_ENTER_MS)
}


onBeforeUnmount(() => {
  if (enemyEnterTimer) clearTimeout(enemyEnterTimer)
})


watch(
  enemyDef,
  (def) => {
    if (!def?.anims?.idle) return
    enemyAfterOnceKey.value = null
    enemyBusy.value = false
    enemyChain.value = null

    // ✅ 등장 연출 중이면 idle로 덮어쓰지 않기
    if (!enemyEnterInProgress.value) {
      applyEnemy("idle")
    }
  },
  { immediate: true }
)

// ✅ finished 핸들러(체인 핵심)
function onEnemyAnimFinished() {
  // 1) hit 끝나면 death로
  if (enemyChain.value === "hit_then_death" && enemyLastOnce.value === "hit") {
    enemyChain.value = "death_then_respawn"
    playOnceEnemy("death")
    return
  }

  // 2) death 끝나면 숨김 → 새 적
  if (enemyChain.value === "death_then_respawn" && enemyLastOnce.value === "death") {
    enemyChain.value = null
    enemyAfterOnceKey.value = null
    enemyBusy.value = false
    enemyVisible.value = false

    if (!pendingFinish.value) {
      spawnOnNext.value = true
    }

    tryCommitFinish()
    return
  }

  // 3) 기본 after 처리
  if (enemyAfterOnceKey.value) {
    applyEnemy(enemyAfterOnceKey.value)
    enemyAfterOnceKey.value = null
  }

  enemyBusy.value = false
  tryCommitFinish()
}

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
  enemyBusy.value = false
  enemyChain.value = null

  // ✅ 다음 문제 없으면 종료(스폰도 안 함)
  if (currentIndex.value + 1 >= quizList.value.length) return
  currentIndex.value++

  // ✅ 여기서만 새 적 등장
  if (spawnOnNext.value) {
    spawnOnNext.value = false
    spawnEnemy()
  } else {
    // 오답 등으로 적이 그대로면 idle 유지
    if (enemyDef.value && enemyVisible.value) applyEnemy("idle")
  }
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
    spawnEnemy()
    
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
    defeatEnemy()
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
