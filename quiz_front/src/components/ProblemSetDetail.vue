<template>
  <div class="text-black p-2">
    <div v-if="loading" class="text-sm text-black/60">불러오는 중...</div>
    <div v-else-if="error" class="text-red-500 text-sm">{{ error }}</div>

    <div v-else-if="quizSet" class="space-y-4">
      <!-- ✅ 헤더 -->
      <div class="flex items-center gap-2 pl-2">
        <h2 class="min-w-0 text-lg font-black leading-snug truncate">
          {{ quizSet.title }}
        </h2>

        <button
          v-if="canEdit"
          class="shrink-0 px-2 input-panel-icon text-xs"
          @click="emit('edit', quizSet.id)"
        >
          수정
        </button>
      </div>

      <!-- ✅ 설명 -->
      <div class="content-panel p-2 pb-8">
        <div class="text-xs  mb-1">설명</div>
        <p class="text-sm whitespace-pre-wrap leading-relaxed text-black/80">
          {{ quizSet.description }}
        </p>
      </div>

      <!-- ✅ 요약 정보 카드들 -->
      <div class="grid grid-cols-3 gap-2">
        <div class="content-panel p-1">
          <div class="text-[11px] text-black/50">작성자</div>
          <div class="text-sm font-bold truncate">
            {{ quizSet.created_by_name ?? "-" }}
          </div>
        </div>

        <div class="content-panel p-1">
          <div class="text-[11px] text-black/50">문제 수</div>
          <div class="text-sm font-bold">
            {{ quizSet.problem_count ?? 0 }}
          </div>
        </div>

        <div class="content-panel p-1">
          <div class="text-[11px] text-black/50">좋아요</div>
          <div class="flex items-center justify-between gap-2">
            <div class="text-sm font-bold">
              {{ quizSet.like_count ?? 0 }}
            </div>

            <!-- GameView 의 체력 표시와 동일하게 이모지 + 투명도로 상태를 나타낸다 -->
            <button
              class="shrink-0 leading-none text-base transition
                     active:scale-90 disabled:active:scale-100"
              :class="quizSet.is_liked ? 'opacity-100' : 'opacity-30'"
              :disabled="liking"
              :aria-pressed="!!quizSet.is_liked"
              :aria-label="quizSet.is_liked ? '좋아요 취소' : '좋아요'"
              @click.stop="toggleLike"
            >
              ❤️
            </button>
          </div>
        </div>
      </div>

      <!-- ✅ 하단 버튼바 -->
      <div class="flex gap-2 pt-1">
        <RouterLink
          :to="{ name: 'game', params: { id: quizSet.id } }"
          class="flex-1 py-2 button-green flex justify-center font-bold"
        >
          Start
        </RouterLink>

        <button
          class="px-4 py-2 button-red font-bold"
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
import { fetchProblemSet } from "@/api/questions"
import { toggleProblemSetLike } from "@/api/game"
import { useAccountStore } from '@/stores/accounts'

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
    const res = await fetchProblemSet(props.quizsetid)
    quizSet.value = res.data
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
    const res = await toggleProblemSetLike(quizSet.value.id)

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