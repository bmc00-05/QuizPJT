<template>
  <div class="text-black h-full min-h-0 flex flex-col px-2">
    <!-- 헤더 -->
    <h1 class="shrink-0 text-base font-semibold mb-2">퀴즈 상세/수정</h1>

    <!-- 상태 -->
    <p v-if="loading" class="text-sm text-gray-600">불러오는 중...</p>
    <p v-else-if="error" class="text-sm text-red-500">{{ error }}</p>

    <!--
      form 을 flex 컨테이너로 삼아 입력 영역만 스크롤시키고 버튼은 하단에 고정한다.
      버튼을 스크롤 영역 안에 sticky 로 두면 배경이 없어 뒤 내용이 비쳐 보인다.
    -->
    <form
      v-else-if="form"
      @submit.prevent="save"
      class="flex-1 min-h-0 flex flex-col"
    >
      <div class="flex-1 min-h-0 overflow-y-auto no-scrollbar space-y-3 pr-1">
        <!-- 문제 -->
        <div>
          <label class="block text-xs font-medium mb-1">문제</label>
          <input v-model="form.question" required class="w-full input-panel-icon px-2 py-1.5 text-sm" />
        </div>

        <!-- 선택지 -->
        <div v-for="i in 4" :key="i">
          <label class="block text-xs font-medium mb-1">선택지 {{ i }}</label>
          <input v-model="form[`choice${i}`]" required class="w-full input-panel-icon px-2 py-1.5 text-sm" />
        </div>

        <!-- 정답 -->
        <div>
          <label class="block text-xs font-medium mb-1">정답</label>
          <select v-model.number="form.answer" required class="w-full input-panel-icon px-2 py-1.5 text-sm">
            <option disabled :value="null">선택</option>
            <option v-for="n in 4" :key="n" :value="n">{{ n }}번</option>
          </select>
        </div>

        <!-- 난이도 -->
        <div>
          <label class="block text-xs font-medium mb-1">난이도</label>
          <select v-model="form.difficulty" required class="w-full input-panel-icon px-2 py-1.5 text-sm">
            <option disabled value="">선택</option>
            <option value="easy">easy</option>
            <option value="medium">medium</option>
            <option value="hard">hard</option>
          </select>
        </div>

        <!-- 해설 -->
        <div>
          <label class="block text-xs font-medium mb-1">해설</label>
          <textarea v-model="form.explanation" rows="3" class="w-full input-panel-icon px-2 py-1.5 text-sm" />
        </div>

      </div>

      <!-- 하단 고정 영역 -->
      <div class="shrink-0 pt-3">
        <p v-if="validationError" class="text-red-500 text-xs mb-2">
          {{ validationError }}
        </p>

        <div class="flex gap-2">
          <button
            type="submit"
            class="flex-1 button-green py-2 disabled:opacity-50"
            :disabled="saving"
          >
            {{ saving ? '저장 중...' : '저장' }}
          </button>

          <button type="button" class="px-2 input-panel-icon" @click="emit('back')">
            뒤로
          </button>

          <button
            type="button"
            class="px-2 button-red disabled:opacity-50"
            @click="remove"
            :disabled="deleting"
          >
            {{ deleting ? '삭제 중...' : '삭제' }}
          </button>
        </div>
      </div>
    </form>

    <p v-else class="text-sm text-gray-600">데이터가 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { fetchProblem, updateProblem, deleteProblem } from "@/api/questions"
import { useDialogStore } from "@/stores/dialog"
import { useAccountStore } from '@/stores/accounts'

const dialog = useDialogStore()

const props = defineProps({
  quizid: { type: [Number, String], required: true },
  // 선택: 있으면 나중에 "문제집에서 제거" 같은 기능 만들 때 유용
  quizsetid: { type: [Number, String], default: null },
})

const emit = defineEmits(['back', 'close', 'saved', 'deleted'])

const accountStore = useAccountStore()

const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const error = ref('')
const validationError = ref('')

// ✅ 단건 API (네 백엔드에 맞게 여기만 조정하면 됨)

const form = ref(null)

const fetchQuiz = async () => {
  if (!props.quizid) return
  loading.value = true
  error.value = ''
  validationError.value = ''
  form.value = null

  try {
    const res = await fetchProblem(props.quizid)

    // 서버 응답 → 수정용 form 구성
    const d = res.data
    form.value = {
      question: d.question ?? '',
      choice1: d.choice1 ?? '',
      choice2: d.choice2 ?? '',
      choice3: d.choice3 ?? '',
      choice4: d.choice4 ?? '',
      answer: d.answer ?? null,
      difficulty: d.difficulty ?? '',
      explanation: d.explanation ?? '',
    }
  } catch (err) {
    console.error(err)
    error.value = '퀴즈 정보를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

const validate = () => {
  validationError.value = ''

  if (!form.value) return false

  if (![1, 2, 3, 4].includes(form.value.answer)) {
    validationError.value = '정답은 1~4번 중에서 선택해야 합니다.'
    return false
  }

  if (!['easy', 'medium', 'hard'].includes(form.value.difficulty)) {
    validationError.value = '난이도를 선택해주세요.'
    return false
  }

  return true
}

const save = async () => {
  if (!form.value) return
  if (!validate()) return

  saving.value = true
  try {
    await updateProblem(props.quizid, { ...form.value })
    emit('saved')
  } catch (err) {
    console.error(err)
    dialog.alert('저장에 실패했습니다.', { tone: 'danger' })
  } finally {
    saving.value = false
  }
}

const remove = async () => {
  const ok = await dialog.confirm("이 문제를 삭제할까요?", {
    tone: "danger",
    confirmText: "삭제",
  })
  if (!ok) return

  deleting.value = true
  try {
    await deleteProblem(props.quizid)
    emit('deleted')
  } catch (err) {
    console.error(err)
    dialog.alert('삭제에 실패했습니다.', { tone: 'danger' })
  } finally {
    deleting.value = false
  }
}

watch(() => props.quizid, fetchQuiz, { immediate: true })
</script>
