<template>
  <div class="h-full w-full min-h-0 flex flex-col gap-1">
    <!-- 상단 패널: 로딩/결과 표시 -->
    <div class="pixel-panel flex-[7] min-h-0">
      <div class="pixel-panel__content p-3 h-full min-h-0 overflow-hidden flex flex-col">
        <div class="shrink-0 flex items-center justify-between mb-2">
          <h1 class="text-black text-lg font-bold">AI 도우미</h1>

          <!-- 무료 AI 티어로 운영되므로 남은 횟수를 미리 알려준다 -->
          <div v-if="quota" class="text-xs text-right leading-tight">
            <div :class="quotaExhausted ? 'text-red-600 font-semibold' : 'text-black/60'">
              남은 코칭 {{ quota.user_remaining }}/{{ quota.user_limit }}회
            </div>
            <div v-if="recoverText" class="text-black/45">
              {{ recoverText }}
            </div>
          </div>
        </div>

        <!-- ✅ 결과/로딩/에러 영역 (스크롤 가능) -->
        <div class="flex-1 input-panel-icon min-h-0 overflow-auto p-3 scroll-slim">
          <!-- 로딩 -->
          <div class="pixel-panel__content p-0">
          <template v-if="coachingLoading">
            <div class="text-sm text-black/80 font-semibold">
              코칭 생성 중<span class="dots"><span>.</span><span>.</span><span>.</span></span>
            </div>
            <div class="mt-2 text-xs text-black/60">
              최근 오답 데이터를 분석하고 있어요. 잠시만 기다려주세요.
            </div>
          </template>

          <!-- 에러 -->
          <template v-else-if="coachingError">
            <div class="text-sm text-red-600 font-semibold">코칭 생성 실패</div>
            <div class="mt-2 text-xs text-red-600/80 whitespace-pre-wrap">
              {{ coachingError }}
            </div>

            <div class="mt-3 flex gap-2">
              <button
                class="px-3 py-2 text-sm rounded border bg-white hover:bg-white/80"
                @click="startCoaching"
              >
                다시 시도
              </button>
              <button
                class="px-3 py-2 text-sm rounded border bg-white hover:bg-white/80"
                @click="clearCoaching"
              >
                지우기
              </button>
            </div>
          </template>

          <!-- 결과 -->
          <template v-else-if="coachingText">
            <!-- 실시간 응답을 받지 못해 예시로 대체된 경우를 명시한다 -->
            <div
              v-if="isDemo"
              class="mb-2 p-2 text-xs text-amber-900 bg-amber-100 border border-amber-300 rounded"
            >
              <b>예시 응답입니다.</b>
              무료 AI 호출량이 모두 소진되었거나 AI 서비스가 일시적으로 응답하지 않아
              미리 준비된 예시를 표시하고 있습니다. 아래 통계는 실제 학습 데이터입니다.
            </div>

            <div class="text-xs text-black/60 mb-2">
              최근 {{ coachingMeta.count }}개 / {{ coachingMeta.from_days }}일 기준
              <span v-if="coachingMeta.model && !isDemo"> · {{ coachingMeta.model }}</span>
            </div>

            <div class="whitespace-pre-wrap text-sm text-black leading-relaxed">
              {{ coachingText }}
            </div>

          </template>

          <!-- 기본 안내 -->
          <template v-else>
            <div class="text-sm text-black/60">
            <b>AI 코칭!</b>을 누르면 여기에서 결과가 표시됩니다.
            </div>
          </template>
        </div>
        </div>
      </div>
    </div>

    <!-- 하단 패널: 입력창 -->
    <div class="pixel-panel flex-[3] min-h-0">
      <div class="pixel-panel__content p-2 pl-3 h-full min-h-0 overflow-hidden flex flex-col">
        <div class="flex items-center justify-between mb-2">
          <h1 class="text-black text-lg font-bold">대화창</h1>
          <div class="text-xs text-black/60">
            {{ extraInput.length }}/500
          </div>
        </div>

        <textarea
          v-model="extraInput"
          class="w-full flex-1 input-panel-icon min-h-0 resize-none no-scrollbar
          p-2 text-sm text-black
              "
          placeholder=
          "AI에게 추가로 요청할 내용을 적어주세요.
          (예: '네트워크 위주로 학습 계획 짜줘')"
          @input="enforceLimit"
          @paste="onPaste"
        />

        <div class="mt-2 text-xs text-black/60">
          * 최대 500자. 비워두면 기본 코칭만 생성돼요.
        </div>
      </div>
    </div>

    <div
      class="shrink-0 w-full button-panel font-bold text-black flex justify-center cursor-pointer select-none"
      :class="coachingLoading || quotaExhausted ? 'opacity-50 pointer-events-none' : ''"
      role="button"
      tabindex="0"
      @click="openConfirm"
      @keydown.enter.prevent="openConfirm"
      @keydown.space.prevent="openConfirm"
    >
      <div class="pixel-panel__content px-4 py-2">
        {{ quotaExhausted ? "오늘 횟수 소진" : "AI 코칭!" }}
      </div>
    </div>

    <!-- ✅ 모달: 경고/확인만 -->
    <BaseModal v-if="modal.isOpen" @close="closeModal">
      <div class="text-black space-y-3">
        <h2 class="text-lg font-bold">AI 코칭 생성</h2>
    <div class="text-sm text-gray-700 space-y-2 whitespace-pre-wrap">
      <p> • 최근 7일 내 오답(최대 20개)을 기반으로 학습 피드백을 생성합니다.</p>
      <p> • 네트워크 상황에 따라 요청 시간이 길어질 수 있습니다.</p>
      <p v-if="quota">
        • 이번 요청 후 남는 횟수: <b>{{ Math.max(0, quota.user_remaining - 1) }}회</b>
        (하루 {{ quota.user_limit }}회)
      </p>
      <p>
        • 사용 횟수는 각 요청으로부터 <b>24시간</b>이 지나면 1회씩 복구됩니다.
      </p>
      <p class="text-red-600 font-medium">※ 오답이 없으면 코칭이 생성되지 않을 수 있습니다.</p>
    </div>
        <p class="text-sm text-black/70 whitespace-pre-wrap">
          최근 오답 기반 코칭을 생성할까요?
          <br />
          <span v-if="extraInput.trim()">
            추가 요청: “{{ extraInput.trim() }}”
          </span>
          <span v-else>
            (추가 요청 없음)
          </span>
        </p>

        <div class="flex justify-end gap-2 pt-2">
          <button
            class="p-1 button-red"
            @click="closeModal"
          >
            취소
          </button>
          <button
            class="p-1 button-green"
            @click="confirmStart"
          >
            확인
          </button>
        </div>
      </div>
    </BaseModal>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import { fetchQuota, requestFeedback } from "@/api/ai"
import { useModalStore } from "@/stores/modal"
import BaseModal from "@/components/common/BaseModal.vue"

const modal = useModalStore()

/**
 * 남은 AI 호출 횟수.
 *
 * 이 서비스는 무료 AI 티어로 운영되므로 호출량이 제한된다.
 * 사용자가 버튼을 누르기 전에 남은 횟수를 알 수 있어야 한다.
 */
const quota = ref(null)

const loadQuota = async () => {
  try {
    const res = await fetchQuota()
    quota.value = res.data
  } catch (e) {
    // 조회 실패는 기능을 막을 이유가 아니다. 표시만 생략한다.
    console.error(e)
    quota.value = null
  }
}

onMounted(loadQuota)

const quotaExhausted = computed(
  () => quota.value !== null && quota.value.user_remaining <= 0
)

/** 사용자당 제한은 롤링 24시간이라 "자정 초기화"가 아니다. */
const recoverText = computed(() => {
  const sec = quota.value?.user_recover_in_sec ?? 0
  if (sec <= 0) return ""
  const hours = Math.floor(sec / 3600)
  const minutes = Math.ceil((sec % 3600) / 60)
  return hours > 0 ? `약 ${hours}시간 후 1회 복구` : `약 ${minutes}분 후 1회 복구`
})

// ✅ 사용자 입력(최대 500자)
const MAX_LEN = 500
const extraInput = ref("")

const enforceLimit = () => {
  if (extraInput.value.length > MAX_LEN) {
    extraInput.value = extraInput.value.slice(0, MAX_LEN)
  }
}

const onPaste = (e) => {
  e.preventDefault()
  const paste = (e.clipboardData || window.clipboardData).getData("text") || ""

  const before = extraInput.value
  const remain = MAX_LEN - before.length
  if (remain <= 0) return

  extraInput.value = before + paste.slice(0, remain)
}

// ✅ 상단 패널에 표시될 상태들
const coachingLoading = ref(false)
const coachingError = ref("")
const coachingText = ref("")
const coachingMeta = ref({ count: 0, from_days: 7, model: "" })
const isDemo = ref(false)

function clearCoaching() {
  coachingLoading.value = false
  coachingError.value = ""
  coachingText.value = ""
  coachingMeta.value = { count: 0, from_days: 7, model: "" }
  isDemo.value = false
}

// ✅ 모달
const openConfirm = () => {
  modal.open(1)
}
const closeModal = () => {
  modal.close()
}

// ✅ "확인" 누르면 모달 닫고 -> 코칭 시작
const confirmStart = () => {
  closeModal()
  startCoaching()
}

// ✅ 실제 코칭 생성 (로딩/결과는 상단 패널로)
const startCoaching = async () => {
  if (coachingLoading.value) return

  coachingLoading.value = true
  coachingError.value = ""
  coachingText.value = ""
  coachingMeta.value = { count: 0, from_days: 7, model: "" }
  isDemo.value = false

  try {
    const res = await requestFeedback({
      days: 7,
      limit: 20,
      extraInput: extraInput.value.trim(),
    })

    const feedback = (res.data.feedback ?? "").trim()
    if (!feedback) {
      coachingError.value = res.data.detail || "피드백이 비어 있습니다."
      return
    }

    coachingText.value = feedback
    isDemo.value = res.data.demo === true
    coachingMeta.value = {
      count: res.data.count ?? 0,
      from_days: res.data.from_days ?? 7,
      model: res.data.model ?? "",
    }
  } catch (e) {
    console.error(e)
    if (e?.response?.status === 429) {
      coachingError.value =
        "오늘 사용 가능한 AI 코칭 횟수를 모두 사용했습니다. 잠시 후 다시 시도해주세요."
    } else {
      coachingError.value = e?.response?.data?.detail || "코칭 생성에 실패했습니다."
    }
  } finally {
    coachingLoading.value = false
    // 호출 후 잔여 횟수를 갱신한다.
    loadQuota()
  }
}
</script>

<style scoped>
/* 요청이 진행 중임을 알리는 점 애니메이션 */
.dots > span {
  opacity: 0;
  animation: dot-appear 1.4s infinite;
}
.dots > span:nth-child(2) { animation-delay: 0.2s; }
.dots > span:nth-child(3) { animation-delay: 0.4s; }

@keyframes dot-appear {
  0%, 20%   { opacity: 0; }
  40%, 100% { opacity: 1; }
}

/* 얇고 눈에 덜 띄는 스크롤바 */
.scroll-slim {
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 0, 0, 0.25) transparent;
}
.scroll-slim::-webkit-scrollbar {
  width: 6px;
}
.scroll-slim::-webkit-scrollbar-track {
  background: transparent;
}
.scroll-slim::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.25);
  border-radius: 3px;
}
.scroll-slim::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.4);
}
</style>
