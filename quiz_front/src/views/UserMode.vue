<template>
  <div class="relative h-full">
    <h1>유저 모드 페이지</h1>

    <ul>
        <li
          v-for="quizset in quizsets"
          :key="quizset.id"
          class="cursor-pointer hover:bg-gray-50"
          @click="openDetail(quizset.id)"
        >
        제목: {{ quizset.title }} <br/>
        좋아요: {{ quizset.like_count }} |
        작성자: {{ quizset.created_by_name }}
        <hr/>
      </li>
    </ul>

    <button
      @click="openModal"
      class="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
    >
      문제집 생성
    </button>

    <BaseModal v-if="modal.isOpen" @close="closeModal">
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
import { useModalStore } from '@/stores/modal'
import axios from 'axios'
import BaseModal from '@/components/common/BaseModal.vue'
import ProblemSetForm from '@/components/ProblemSetForm.vue'
import ProblemSetCreate from '@/components/ProblemSetCreate.vue'
import QuizCreate from '@/components/QuizCreate.vue'
import ProblemSetDetail from '@/components/ProblemSetDetail.vue'

const API_URL = import.meta.env.VITE_REST_API_URL
const modal = useModalStore()
const accountStore = useAccountStore()

const currentQuizsetId = ref(null)

const quizsets = ref([])

// ✅ 모달 내용 교체용
const modalView = shallowRef(ProblemSetForm)
const modalProps = ref({})

const extraListeners = computed(() => {
  const name = modalView.value?.__name   // ✅ 컴포넌트 이름으로 판별
  ////나중에 문제 가능 표식/////////////////
  if (name === 'ProblemSetCreate' || name === 'ProblemSetDetail') {
    return { updated: onUpdated, goCreateQuiz: onGoCreateQuiz, edit: onEditProblemSet }
  }
  
  if (name === 'QuizCreate') {
    return { done: backToProblemSetCreate }
  }
  return {}
})
  
const getProblemSets = async () => {
  const res = await axios.get(`${API_URL}/game/users/problemsets/`, {
    headers: { Authorization: `Token ${accountStore.token}` },
  })
  quizsets.value = res.data
}

// ✅ 생성 버튼 → 생성 폼 모달
const openModal = () => {
  modalView.value = ProblemSetForm
  modalProps.value = {}
  modal.open(1)
}

// ✅ 생성 성공 → 디테일/수정 모달로 전환 (props 이름 맞추기!)
const onCreated = (createdId) => {
  currentQuizsetId.value = createdId 
  modalView.value = ProblemSetCreate
  modalProps.value = { quizsetid: createdId } // ✅ 여기!
}

// ✅ 디테일에서 저장 완료 시 목록 갱신 (선택)
const onUpdated = () => {
  getProblemSets()
}

const closeModal = () => modal.close()

const onGoCreateQuiz = (quizsetId) => {
  console.log('modalView=', modalView.value, 'modalProps=', modalProps.value)
  console.log('onGoCreateQuiz fired:', quizsetId)
  currentQuizsetId.value = quizsetId
  modalView.value = QuizCreate
  modalProps.value = { quizsetid: quizsetId } // ✅ QuizCreate가 받을 props
}

const backToProblemSetCreate = () => {
  modalView.value = ProblemSetCreate
  modalProps.value = { quizsetid: currentQuizsetId.value }
}

const onEditProblemSet = (quizsetId) => {
  currentQuizsetId.value = quizsetId
  modalView.value = ProblemSetCreate
  modalProps.value = { quizsetid: quizsetId }
}

const openDetail = (quizsetId) => {
  currentQuizsetId.value = quizsetId
  modalView.value = ProblemSetDetail
  modalProps.value = { quizsetid: quizsetId }
  modal.open(1)
}

onMounted(getProblemSets)
</script>
