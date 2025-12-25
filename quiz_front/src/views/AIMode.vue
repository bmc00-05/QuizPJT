<template>
  <div class="h-full w-full min-h-0 flex flex-col gap-1">
    <!-- 상단 패널: 로딩/결과 표시 -->
    <div class="pixel-panel flex-[7] min-h-0">
      <div class="pixel-panel__content p-3 h-full min-h-0 overflow-hidden flex flex-col">
        <div class="shrink-0">
          <h1 class="text-black text-lg font-bold mb-2">AI 모드</h1>

        </div>

        <!-- ✅ 결과/로딩/에러 영역 (스크롤 가능) -->
        <div class="flex-1 input-panel-icon min-h-0 overflow-auto p-3">
          <!-- 로딩 -->
          <div class="pixel-panel__content p-0">
          <template v-if="coachingLoading">
            <div class="text-sm text-black/80 font-semibold">코칭 생성 중...</div>
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
            <div class="text-xs text-black/60 mb-2">
              최근 {{ coachingMeta.count }}개 / {{ coachingMeta.from_days }}일 기준
              <span v-if="coachingMeta.model"> · {{ coachingMeta.model }}</span>
            </div>

            <div class="whitespace-pre-wrap text-sm text-black leading-relaxed">
              {{ coachingText }}
            </div>

            <div class="mt-3 flex gap-2">
              <button
                class="px-3 py-2 text-sm text-black rounded border bg-white hover:bg-white/80"
                @click="startCoaching"
              >
                새로 생성
              </button>
              <button
                class="px-3 py-2 text-sm text-black rounded border bg-white hover:bg-white/80"
                @click="clearCoaching"
              >
                지우기
              </button>
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
          class="w-full flex-1 input-panel-icon min-h-0 resize-none
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
      :class="coachingLoading ? 'opacity-50 pointer-events-none' : ''"
      role="button"
      tabindex="0"
      @click="openConfirm"
      @keydown.enter.prevent="openConfirm"
      @keydown.space.prevent="openConfirm"
    >
      <div class="pixel-panel__content px-4 py-2">
        AI 코칭!
      </div>
    </div>

    <!-- ✅ 모달: 경고/확인만 -->
    <BaseModal v-if="modal.isOpen" @close="closeModal">
      <div class="text-black space-y-3">
        <h2 class="text-lg font-bold">AI 코칭 생성</h2>
    <div class="text-sm text-gray-700 space-y-2 whitespace-pre-wrap">
      <p>• 최근 7일 내 오답(최대 20개)을 기반으로 학습 피드백을 생성합니다.</p>
      <p>• 생성된 피드백은 참고용이며, 최종 판단은 본인이 확인해야 합니다.</p>
      <p>• 네트워크 상황에 따라 요청 시간이 길어질 수 있습니다.</p>
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
            class="px-3 py-2 rounded border bg-white hover:bg-white/80"
            @click="closeModal"
          >
            취소
          </button>
          <button
            class="px-3 py-2 rounded bg-black text-white hover:opacity-90"
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
import { ref } from "vue"
import axios from "axios"
import { useAccountStore } from "@/stores/accounts"
import { useModalStore } from "@/stores/modal"
import BaseModal from "@/components/common/BaseModal.vue"

const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()
const modal = useModalStore()

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

function clearCoaching() {
  coachingLoading.value = false
  coachingError.value = ""
  coachingText.value = ""
  coachingMeta.value = { count: 0, from_days: 7, model: "" }
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

  try {
    const res = await axios.post(
      `${API_URL}/ai/feedback/`,
      {
        days: 7,
        limit: 20,
        extra_input: extraInput.value.trim(),
      },
      { headers: { Authorization: `Token ${accountStore.token}` } }
    )

    const feedback = (res.data.feedback ?? "").trim()
    if (!feedback) {
      coachingError.value = res.data.detail || "피드백이 비어 있습니다."
      return
    }

    coachingText.value = feedback
    coachingMeta.value = {
      count: res.data.count ?? 0,
      from_days: res.data.from_days ?? 7,
      model: res.data.model ?? "",
    }
  } catch (e) {
    console.error(e)
    coachingError.value = e?.response?.data?.detail || "코칭 생성에 실패했습니다."
  } finally {
    coachingLoading.value = false
  }
}
</script>

<style scoped>
</style>
