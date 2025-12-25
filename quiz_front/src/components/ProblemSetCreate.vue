<template>
  <div class="text-black">
    <template v-if="quizSet">
      <div class="text-xs text-black/60 mb-2">No. {{ quizSet.id }}</div>

      <form @submit.prevent="updateQuizSet" class="space-y-3">
        <!-- 제목 -->
        <div class="space-y-1">
          <div class="text-xs font-bold text-black/70">제목</div>
          <input
            v-model="quizSet.title"
            class="w-full input-panel-icon outline-none"
            placeholder="제목"
          />
        </div>

        <!-- 설명 -->
        <div class="space-y-1">
          <div class="text-xs font-bold text-black/70">설명</div>
          <textarea
            v-model="quizSet.description"
            class="w-full input-panel-icon outline-none resize-none min-h-[96px]"
            placeholder="설명"
          />
        </div>

        <!-- ✅ 저장 / 삭제: 양옆 배치 -->
        <div class="flex items-center justify-between pt-2">
          <button
            type="submit"
            class="px-3 py-1.5 border rounded text-sm font-bold"
          >
            저장
          </button>

          <button
            type="button"
            class="px-3 py-1.5 border rounded text-sm font-bold text-red-600"
            @click="deleteQuizSet"
          >
            삭제
          </button>
        </div>
      </form>

      <hr class="my-3" />

      <!-- ✅ 문제 목록 -->
      <QuizList
        :quizSetId="quizSet.id"
        @select="onSelectQuiz"
        @changed="refreshQuizSetProblems"
      />

      <!-- ✅ 문제 추가: 중앙 정렬 -->
      <div class="mt-4 flex justify-center">
        <button
          class="px-4 py-2 input-panel-icon font-bold"
          @click="goCreateQuiz"
        >
          문제 추가
        </button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { useRoute } from 'vue-router'
import axios from 'axios'
import QuizList from '@/components/QuizList.vue'

const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()
const route = useRoute()

// ✅ openQuizDetail 추가 (퀴즈 상세도 모달로 띄울 거면)
const emit = defineEmits(['updated', 'goCreateQuiz', 'openQuizDetail', 'deleted', 'close'])

const props = defineProps({
  quizsetid: { type: [String, Number], default: null },
})

const quizSetId = computed(() => props.quizsetid ?? route.params.quizsetid)
const quizSet = ref(null)

const getQuizSet = async (id) => {
  if (!id) return
  try {
    const res = await axios.get(`${API_URL}/questions/problemsets/${id}/`, {
      headers: { Authorization: `Token ${accountStore.token}` },
    })
    quizSet.value = res.data
  } catch (err) {
    console.error('문제집 조회 실패:', err)
    quizSet.value = null
  }
}

const updateQuizSet = async () => {
  if (!quizSet.value || !quizSetId.value) return

  try {
    const res = await axios.patch(
      `${API_URL}/questions/problemsets/${quizSetId.value}/`,
      { title: quizSet.value.title, description: quizSet.value.description },
      { headers: { Authorization: `Token ${accountStore.token}` } }
    )

    quizSet.value = res.data
    emit('updated')
    alert('문제집 수정 완료')
  } catch (err) {
    console.error(err)
    alert('문제집 수정 실패')
  }
}

const deleteQuizSet = async () => {
  if (!quizSetId.value) return

  const ok = confirm("정말 이 문제집을 삭제할까요? (복구 불가)")
  if (!ok) return

  try {
    await axios.delete(`${API_URL}/questions/problemsets/${quizSetId.value}/`, {
      headers: { Authorization: `Token ${accountStore.token}` },
    })

    alert("문제집 삭제 완료")

    // ✅ 부모에서 목록 다시 불러오게
    emit("deleted", quizSetId.value)
    emit("updated")

    // ✅ 모달로 띄우는 구조라면 닫기 이벤트도 보내기
    emit("close")
  } catch (err) {
    console.error(err)
    alert("문제집 삭제 실패")
  }
}

const goCreateQuiz = () => {
  emit('goCreateQuiz', quizSet.value.id)
}

// ✅ QuizList에서 퀴즈 클릭하면 여기로 들어옴
const onSelectQuiz = (quizId) => {
  emit('openQuizDetail', {
    quizId,
    quizSetId: quizSetId.value,   // computed로 갖고 있는 문제집 id
  })
}

const refreshQuizSetProblems = () => {
  getQuizSet(quizSetId.value)
}

watch(quizSetId, (id) => getQuizSet(id), { immediate: true })
</script>
<style scoped>

</style>