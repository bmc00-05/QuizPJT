<template>
  <div class="h-full w-full min-h-0 flex flex-col gap-2">
    <!-- 상단 패널 -->
    <div class="pixel-panel flex-[7] min-h-0">
      <div class="pixel-panel__content h-full min-h-0 overflow-hidden">
        <h1 class="text-black text-lg font-bold mb-3">AI 모드</h1>

        <!-- 여기에 추가로 AI 요약/최근 기록 등을 넣어도 됨 -->
        <p class="text-black/70 text-sm">
          최근 오답 기반 코칭 + (선택) 사용자 추가 요청을 반영합니다.
        </p>
      </div>
    </div>

    <!-- 하단 패널: 입력창 -->
    <div class="pixel-panel m-2 flex-[3] min-h-0">
      <div class="pixel-panel__content h-full min-h-0 overflow-hidden flex flex-col">
        <div class="flex items-center justify-between mb-2">
          <h1 class="text-black text-lg font-bold">대화창</h1>
          <div class="text-xs text-black/60">
            {{ extraInput.length }}/500
          </div>
        </div>

        <textarea
          v-model="extraInput"
          class="w-full flex-1 min-h-0 resize-none
                 rounded border border-black/20
                 bg-white/80 p-2 text-sm text-black
                 focus:outline-none focus:ring-2 focus:ring-black/20"
          placeholder="AI에게 추가로 요청할 내용을 적어주세요. (예: '네트워크 위주로 학습 계획 짜줘')"
          @input="enforceLimit"
          @paste="onPaste"
        />

        <div class="mt-2 text-xs text-black/60">
          * 최대 500자. 비워두면 기본 코칭만 생성돼요.
        </div>
      </div>
    </div>

    <!-- 버튼은 맨 아래 고정 -->
    <div class="m-2 shrink-0 button-panel font-bold text-black flex justify-center">
      <button
        class="pixel-panel__content px-4 py-2"
        @click="openCoachingIntro"
      >
        AI 코칭!
      </button>
    </div>

    <!-- 모달 -->
    <BaseModal v-if="modal.isOpen" @close="closeModal">
      <component
        :is="modalView"
        v-bind="modalProps"
        @close="closeModal"
        v-on="extraListeners"
      />
    </BaseModal>
  </div>
</template>

<script setup>
import { shallowRef, ref, computed } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import { useModalStore } from '@/stores/modal'

import BaseModal from '@/components/common/BaseModal.vue'
import AICoachIntro from '@/components/AICoachIntro.vue'
import AIFeedbackModal from '@/components/AIFeedbackModal.vue'

const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()
const modal = useModalStore()

// ✅ 사용자 입력(최대 500자)
const MAX_LEN = 500
const extraInput = ref('')

// 모달 구성
const modalView = shallowRef(AICoachIntro)
const modalProps = ref({ loading: false, error: '' })

const feedbackState = ref({
  feedback: '',
  meta: { count: 0, from_days: 7, model: '' },
})

const extraListeners = computed(() => {
  if (modalView.value === AICoachIntro) return { start: onStartCoaching }
  if (modalView.value === AIFeedbackModal) return { retry: onRetry }
  return {}
})

const enforceLimit = () => {
  if (extraInput.value.length > MAX_LEN) {
    extraInput.value = extraInput.value.slice(0, MAX_LEN)
  }
}

const onPaste = (e) => {
  // 붙여넣기에서도 500자 강제
  e.preventDefault()
  const paste = (e.clipboardData || window.clipboardData).getData('text') || ''

  const before = extraInput.value
  const remain = MAX_LEN - before.length
  if (remain <= 0) return

  extraInput.value = before + paste.slice(0, remain)
}

const openCoachingIntro = () => {
  modalView.value = AICoachIntro
  modalProps.value = { loading: false, error: '' }
  modal.open(1)
}

const closeModal = () => {
  modal.close()
  modalProps.value = { loading: false, error: '' }
  feedbackState.value = { feedback: '', meta: { count: 0, from_days: 7, model: '' } }
}

// ✅ "start" 누르면: extra_input 포함해서 서버 호출
const onStartCoaching = async () => {
  modalProps.value = { ...modalProps.value, loading: true, error: '' }

  try {
    const res = await axios.post(
      `${API_URL}/ai/feedback/`, // ✅ 네 엔드포인트에 맞게 유지/수정
      {
        days: 7,
        limit: 20,
        extra_input: extraInput.value.trim(), // ✅ 추가 입력 반영
      },
      { headers: { Authorization: `Token ${accountStore.token}` } }
    )

    const feedback = (res.data.feedback ?? '').trim()

    if (!feedback) {
      modalProps.value = {
        ...modalProps.value,
        loading: false,
        error: res.data.detail || '피드백이 비어 있습니다.',
      }
      return
    }

    feedbackState.value = {
      feedback,
      meta: {
        count: res.data.count ?? 0,
        from_days: res.data.from_days ?? 7,
        model: res.data.model ?? '',
      },
    }

    modalView.value = AIFeedbackModal
    modalProps.value = {
      feedback: feedbackState.value.feedback,
      meta: feedbackState.value.meta,
    }
  } catch (e) {
    console.error(e)
    modalProps.value = {
      ...modalProps.value,
      loading: false,
      error: e?.response?.data?.detail || '코칭 생성에 실패했습니다.',
    }
  } finally {
    if (modalView.value?.__name === 'AICoachIntro') {
      modalProps.value = { ...modalProps.value, loading: false }
    }
  }
}

const onRetry = () => {
  modalView.value = AICoachIntro
  modalProps.value = { loading: false, error: '' }
  onStartCoaching()
}
</script>

<style scoped>
</style>
