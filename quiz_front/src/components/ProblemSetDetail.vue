<template>
  <div class="text-black p-2">
    <div v-if="loading" class="text-sm text-black/60">불러오는 중...</div>
    <div v-else-if="error" class="text-red-500 text-sm">{{ error }}</div>

    <div v-else-if="quizSet" class="space-y-4">
      <!-- ✅ 헤더 -->
      <div class="flex items-start justify-between  gap-3">
        <div class="min-w-0">
          <div class="text-xs text-black/50">ProblemSet #{{ quizSet.id }}</div>
          <h2 class="text-lg font-black leading-snug truncate">
            {{ quizSet.title }}
          </h2>
        </div>

        <button
          v-if="canEdit"
          class="shrink-0 mr-5 mt-3 px-2 input-panel-icon text-xs"
          @click="emit('edit', quizSet.id)"
        >
          수정
        </button>
      </div>

      <!-- ✅ 설명 -->
      <div class="input-panel-icon p-2 pb-8">
        <div class="text-xs  mb-1">설명</div>
        <p class="text-sm whitespace-pre-wrap leading-relaxed text-black/80">
          {{ quizSet.description }}
        </p>
      </div>

      <!-- ✅ 요약 정보 카드들 -->
      <div class="grid grid-cols-3 gap-2">
        <div class="input-panel-icon p-1">
          <div class="text-[11px] text-black/50">작성자</div>
          <div class="text-sm font-bold truncate">
            {{ quizSet.created_by_name ?? "-" }}
          </div>
        </div>

        <div class="input-panel-icon p-1">
          <div class="text-[11px] text-black/50">문제 수</div>
          <div class="text-sm font-bold">
            {{ quizSet.problem_count ?? 0 }}
          </div>
        </div>

        <div class="input-panel-icon p-1">
          <div class="text-[11px] text-black/50">좋아요</div>
          <div class="flex items-center justify-between gap-2">
            <div class="text-sm font-bold">
              {{ quizSet.like_count ?? 0 }}
            </div>

            <button
              class="px-2 py-1 border rounded text-[11px] disabled:opacity-40"
              :disabled="liking"
              @click.stop="toggleLike"
            >
              {{ quizSet.is_liked ? "♥" : "♡" }}
            </button>
          </div>
        </div>
      </div>

      <!-- ✅ 하단 버튼바 -->
      <div class="flex gap-2 pt-1">
        <RouterLink
          :to="{ name: 'game', params: { id: quizSet.id } }"
          class="flex-1 py-2 rounded text-center font-bold bg-blue-600 text-white"
        >
          Start
        </RouterLink>

        <button
          class="px-4 py-2 border rounded font-bold"
          @click="emit('close')"
        >
          닫기
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()

const props = defineProps({
  quizsetid: { type: [String, Number], required: true },
})

const emit = defineEmits(['close', 'start', 'edit'])

const quizSet = ref(null)
const loading = ref(false)
const error = ref('')

const fetchDetail = async () => {
  loading.value = true
  error.value = ''
  quizSet.value = null


  try {
    const res = await axios.get(`${API_URL}/questions/problemsets/${props.quizsetid}/`, {
      headers: { Authorization: `Token ${accountStore.token}` },
    })
    quizSet.value = res.data

    // ✅ 미리보기(선택): 문제 목록 API가 있으면 3개만 가져오기
    // 백엔드가 지원한다면:
    // const p = await axios.get(`${API_URL}/questions/problemsets/${props.quizsetid}/problems/`, ...)
    // preview.value = p.data.slice(0, 3)
  } catch (err) {
    console.error(err)
    error.value = '문제집 정보를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

watch(() => props.quizsetid, fetchDetail, { immediate: true })

const canEdit = computed(() => {
  if (!quizSet.value) return false

  // ✅ 1) created_by(id)가 응답에 있으면 이게 제일 정확
  if (quizSet.value.created_by != null && accountStore.user?.pk != null) {
    return Number(quizSet.value.created_by) === Number(accountStore.user.pk)
  }
  return false
})

const liking = ref(false)

const toggleLike = async () => {
  if (!quizSet.value || liking.value) return
  liking.value = true
  try {
    const res = await axios.post(
      `${API_URL}/game/problemsets/${quizSet.value.id}/like/`,
      {},
      { headers: { Authorization: `Token ${accountStore.token}` } }
    )

    // 응답: { liked, like_count, problemset_id }
    quizSet.value.is_liked = res.data.liked
    quizSet.value.like_count = res.data.like_count
  } catch (err) {
    console.error(err)
    error.value = '좋아요 처리에 실패했습니다.'
  } finally {
    liking.value = false
  }
}
</script>