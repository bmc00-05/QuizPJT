<template>
  <div class="h-full w-full min-h-0 flex flex-col text-black">
    <!-- Header -->
    <header class="shrink-0 px-4 pt-4 pb-2">
      <div class="mx-auto w-full max-w-[360px] text-center">
        <h2 class="font-bold text-xl">나의 문제집</h2>
        <p class="text-[11px] opacity-70 mt-1">클릭하면 상세/편집 화면으로 이동</p>
      </div>
    </header>

    <!-- List -->
    <main class="flex-1 min-h-0 px-4 pb-2 flex justify-center">
      <div class="w-full max-w-[360px] min-h-0">
        <!-- ✅ 패널 프레임 -->
        <div class="h-full min-h-0">
          <!-- ✅ 실제 스크롤은 여기 -->
          <div
            class="h-full min-h-0 p-2 overflow-y-auto pr-1 max-h-[360px] no-scrollbar"


          >
            <ul class="flex flex-col gap-2">
              <li v-for="quizset in quizSets" :key="quizset.id">
                <button
                  type="button"
                  class="w-full input-panel-icon px-3 py-2 text-left
                         transition-transform active:scale-[0.99]"
                  @click="openDetail(quizset.id)"
                >
                  <div class="flex items-center justify-between gap-2">
                    <div class="min-w-0">
                      <div class="font-semibold text-[13px] leading-snug truncate">
                        {{ quizset.title }}
                      </div>
                      <div class="text-[11px] opacity-70 mt-0.5">
                        좋아요 {{ quizset.like_count }}
                      </div>
                    </div>

                    <span class="text-[11px] opacity-70 shrink-0">
                      ▶
                    </span>
                  </div>
                </button>
              </li>

              <li v-if="!quizSets.length" class="text-center text-[11px] opacity-70 py-6">
                아직 문제집이 없습니다. 아래에서 만들어보세요!
              </li>
            </ul>
          </div>
        </div>
      </div>
    </main>

    <!-- Bottom action bar -->
    <footer class="shrink-0 px-4 pb-4 pt-2">
      <div class="mx-auto w-full max-w-[360px] flex justify-center gap-2">
        <button
          type="button"
          @click="openModal"
          class="button-panel w-full max-w-[160px]"
        >
          <div class="pixel-panel__content p-2 text-center font-bold">문제집 생성</div>
        </button>

        <button
          v-if="showClose"
          type="button"
          class="button-panel w-full max-w-[120px]"
          @click="$emit('close')"
        >
          <div class="pixel-panel__content p-2 text-center font-bold">닫기</div>
        </button>
      </div>
    </footer>

    <!-- Modal -->
    <BaseModal v-if="innerOpen" @close="closeModal">
      <component
        :is="modalView"
        v-bind="modalProps"
        @created="onCreated"
        @close="closeModal"
        v-on="extraListeners"
      />
    </BaseModal>
  </div>
</template>


<script setup>
import { ref, onMounted, shallowRef, computed } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

import BaseModal from '@/components/common/BaseModal.vue'
import ProblemSetForm from '@/components/ProblemSetForm.vue'
import ProblemSetCreate from '@/components/ProblemSetCreate.vue'
import QuizCreate from '@/components/QuizCreate.vue'
import ProblemSetDetail from '@/components/ProblemSetDetail.vue'
import QuizDetail from '@/components/QuizDetail.vue'

const emit = defineEmits(['close'])

const props = defineProps({
  // ✅ 프로필 모달에서 띄울 때만 true로 넘기면 “닫기” 버튼이 나타남
  showClose: { type: Boolean, default: false },
})

const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()

const quizSets = ref([])
const currentQuizsetId = ref(null)

// ✅ (중요) 기존 modal store 대신 로컬 boolean
const innerOpen = ref(false)

// ✅ 모달 교체
const modalView = shallowRef(ProblemSetForm)
const modalProps = ref({})

// ✅ 모달별 이벤트 라우팅
const extraListeners = computed(() => {
  // __name에 의존하면 빌드/옵션에 따라 undefined일 수 있어서
  // 컴포넌트 레퍼런스로 비교하는 게 더 안전함
  const view = modalView.value

  if (view === ProblemSetCreate || view === ProblemSetDetail) {
    return {
      updated: onUpdated,
      goCreateQuiz: onGoCreateQuiz,
      edit: onEditProblemSet,
      openQuizDetail: onOpenQuizDetail,
    }
  }

  if (view === QuizCreate) {
    return { done: backToProblemSetCreate }
  }

  if (view === QuizDetail) {
    return {
      back: backToProblemSetCreate,
      saved: backToProblemSetCreate,
      deleted: backToProblemSetCreate,
      close: closeModal,
    }
  }

  return {}
})

// ✅ 목록 조회
const getQuizSets = async () => {
  try {
    const res = await axios.get(`${API_URL}/questions/problemsets/`, {
      headers: { Authorization: `Token ${accountStore.token}` },
    })
    quizSets.value = res.data
  } catch (err) {
    console.error(err)
  }
}

// ✅ 생성 모달
const openModal = () => {
  modalView.value = ProblemSetForm
  modalProps.value = {}
  innerOpen.value = true
}

// ✅ 생성 완료 → 관리 모달
const onCreated = (createdId) => {
  currentQuizsetId.value = createdId
  modalView.value = ProblemSetCreate
  modalProps.value = { quizsetid: createdId }
}

// ✅ 수정 저장 완료 시 목록 갱신
const onUpdated = () => {
  getQuizSets()
}

const closeModal = () => {
  innerOpen.value = false
}

// ✅ 문제 추가로 이동
const onGoCreateQuiz = (quizsetId) => {
  currentQuizsetId.value = quizsetId
  modalView.value = QuizCreate
  modalProps.value = { quizsetid: quizsetId }
}

// ✅ 퀴즈 생성 완료 → 다시 문제집 관리로
const backToProblemSetCreate = () => {
  modalView.value = ProblemSetCreate
  modalProps.value = { quizsetid: currentQuizsetId.value }
}

// ✅ 상세에서 수정 버튼 눌렀을 때 → 관리 화면으로
const onEditProblemSet = (quizsetId) => {
  currentQuizsetId.value = quizsetId
  modalView.value = ProblemSetCreate
  modalProps.value = { quizsetid: quizsetId }
}

// ✅ QuizList에서 quiz 클릭 → QuizDetail로 전환
const onOpenQuizDetail = ({ quizId, quizSetId }) => {
  currentQuizsetId.value = quizSetId
  modalView.value = QuizDetail
  modalProps.value = { quizid: quizId, quizsetid: quizSetId }
}

// ✅ 목록 클릭 → 상세 모달
const openDetail = (quizsetId) => {
  currentQuizsetId.value = quizsetId
  modalView.value = ProblemSetDetail
  modalProps.value = { quizsetid: quizsetId }
  innerOpen.value = true
}

onMounted(getQuizSets)
</script>
<style scoped>
/* no-scrollbar 유틸 */
.no-scrollbar::-webkit-scrollbar {
  display: none; /* Chrome/Safari/Edge */
}
.no-scrollbar {
  -ms-overflow-style: none;  /* IE/old Edge */
  scrollbar-width: none;     /* Firefox */
}</style>