<template>
  <div class="h-full w-full min-h-0 flex flex-col text-black">
    <!-- 전체 패널(카드) -->
    <div class="flex h-full">
    <div class="pixel-panel w-full mx-auto flex-1 min-h-0 flex flex-col">
    <!-- <div class="pixel-panel m-2 w-full max-w-[420px] flex-1 min-h-0 flex flex-col"> -->

<!-- 헤더(고정) -->
<div class="px-4 pt-2 pb-2">
  <!-- ✅ 타이틀: 중앙 고정 + 좌/우 버튼은 바닥에 -->
  <div class="relative h-10 ">
    <!-- 왼쪽 버튼(바닥 붙임) -->
    <div class="absolute left-0 bottom-0">
      <button
        class="text-xs input-panel-icon px-1  ml-2 disabled:opacity-40"
        :disabled="loading"
        @click="toggleSort"
      >
        {{ sortLabel }}
      </button>
    </div>

    <!-- 가운데 타이틀(진짜 중앙) -->
    <h1 class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 text-xl font-bold tracking-wide">
      유저 문제집
    </h1>

    <!-- 오른쪽 버튼(바닥 붙임) -->
    <div class="absolute right-0 bottom-0">
      <button
        class="text-xs input-panel-icon mr-2"
        @click="openModal"
      >
        문제집 생성
      </button>
    </div>
  </div>
</div>

<div class="pixel-panel__content pt-2 flex-1 min-h-0 overflow-y-auto">
  <ul class="divide-y divide-black/15">
    <li
      v-for="quizset in pagedQuizsets"
      :key="quizset.id"
      class="cursor-pointer"
      @click="openDetail(quizset.id)"
    >
      <!-- ✅ 얇은 선 바운더리 + 살짝 패딩만 -->
      <div
        class="mx-2 my-1 input-panel-content border-black/20 bg-white/40
               px-3 py-2 hover:bg-white/60 transition"
      >
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0">
            <div class="text-sm font-bold truncate">
              {{ quizset.title }}
            </div>
            <div class="text-xs text-black/70 mt-1">
              작성자: {{ quizset.created_by_name }}
            </div>
          </div>

          <div class="shrink-0 text-xs text-black/70">
            ❤️ {{ quizset.like_count }}
          </div>
        </div>
      </div>
    </li>
  </ul>
</div>

      <!-- 페이지네이션(고정) -->
      <div v-if="totalPages > 1" class="shrink-0 flex items-center justify-between gap-2 px-2 py-2">
        <button
          class="px-3 py-1 ml-5 input-panel-icon disabled:opacity-40"
          :disabled="page === 1"
          @click="page--"
        >
          이전
        </button>

        <div class="text-sm">
          {{ page }} / {{ totalPages }}
        </div>

        <button
          class="px-3 py-1 mr-5 input-panel-icon disabled:opacity-70"
          :disabled="page === totalPages"
          @click="page++"
        >
          다음
        </button>
      </div>
    </div>
    </div>

    <!-- 모달 -->
<BaseModal v-if="modal.isOpen" @close="popOrCloseModal">
  <component
    :is="modalView"
    v-bind="modalProps"
    @created="onCreated"
    @close="popOrCloseModal"
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
import QuizDetail from '@/components/QuizDetail.vue'

const API_URL = import.meta.env.VITE_REST_API_URL
const modal = useModalStore()
const accountStore = useAccountStore()

const currentQuizsetId = ref(null)
const quizsets = ref([])

const page = ref(1)
const pageSize = 5

// ✅ 정렬 (기본 좋아요순)
const sort = ref('like')

// ✅ 로딩(연타 방지 + UX)
const loading = ref(false)

const sortLabel = computed(() => (sort.value === 'like' ? '최신순' : '좋아요순'))

const getProblemSets = async () => {
  loading.value = true
  try {
    const res = await axios.get(`${API_URL}/game/users/problemsets/`, {
      params: { sort: sort.value },
      headers: { Authorization: `Token ${accountStore.token}` },
    })
    quizsets.value = res.data
    page.value = 1
  } catch (err) {
    console.log(err)
  } finally {
    loading.value = false
  }
}

const toggleSort = async () => {
  if (loading.value) return
  sort.value = sort.value === 'like' ? 'recent' : 'like'
  await getProblemSets()
}

// ✅ 모달 내용 교체용
const modalView = shallowRef(ProblemSetForm)
const modalProps = ref({})

const extraListeners = computed(() => {
  const name = modalView.value?.__name

  if (name === 'ProblemSetCreate' || name === 'ProblemSetDetail') {
    return {
      updated: onUpdated,
      goCreateQuiz: onGoCreateQuiz,
      edit: onEditProblemSet,
      openQuizDetail: onOpenQuizDetail,
    }
  }

  if (name === 'QuizCreate') return { done: popOrCloseModal }

  if (name === 'QuizDetail') {
    return { back: popOrCloseModal, saved: popOrCloseModal, deleted: popOrCloseModal }
  }

  return {}
})






const onUpdated = async () => {
  await getProblemSets()
}

const closeModal = () => modal.close()



const backToProblemSetCreate = () => {
  modalView.value = ProblemSetCreate
  modalProps.value = { quizsetid: currentQuizsetId.value }
}

const onEditProblemSet = (quizsetId) => {
  currentQuizsetId.value = quizsetId
  modalView.value = ProblemSetCreate
  modalProps.value = { quizsetid: quizsetId }
}



const totalPages = computed(() => Math.max(1, Math.ceil(quizsets.value.length / pageSize)))

const pagedQuizsets = computed(() => {
  const start = (page.value - 1) * pageSize
  return quizsets.value.slice(start, start + pageSize)
})

// 모달

const modalStack = ref([])

const openRootModal = (view, props = {}) => {
  modalStack.value = []          // 루트로 열 때는 히스토리 초기화
  modalView.value = view
  modalProps.value = props
  modal.open(1)
}


const onOpenQuizDetail = ({ quizId, quizSetId }) => {
  currentQuizsetId.value = quizSetId
  pushModal(QuizDetail, { quizid: quizId, quizsetid: quizSetId }) // ✅ 여기!
}

const onGoCreateQuiz = (quizsetId) => {
  currentQuizsetId.value = quizsetId
  pushModal(QuizCreate, { quizsetid: quizsetId })   // ✅ 여기!
}

const pushModal = (nextView, nextProps = {}) => {
  // 현재 화면을 스택에 저장하고 다음 화면으로 전환
  modalStack.value.push({
    view: modalView.value,
    props: modalProps.value,
  })
  modalView.value = nextView
  modalProps.value = nextProps
}

const popOrCloseModal = () => {
  const prev = modalStack.value.pop()
  if (prev) {
    modalView.value = prev.view
    modalProps.value = prev.props
  } else {
    modal.close()
  }
}

const onCreated = (createdId) => {
  currentQuizsetId.value = createdId
  pushModal(ProblemSetCreate, { quizsetid: createdId })
}

const openModal = () => {
  openRootModal(ProblemSetForm, {})
}

const openDetail = (quizsetId) => {
  currentQuizsetId.value = quizsetId
  openRootModal(ProblemSetDetail, { quizsetid: quizsetId })
}

onMounted(getProblemSets)
</script>
