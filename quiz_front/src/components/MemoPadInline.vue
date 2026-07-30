<template>
  <div class="h-full min-h-0 flex flex-col gap-2 text-black">
    <!-- ✅ 헤더: 타이틀 + (오른쪽) 버튼 나열 -->
    <div class="flex items-center justify-between gap-2 shrink-0">
      <div class="flex items-center gap-2 min-w-0">
        <div class="font-bold ml-2 text-sm shrink-0">메모</div>

        <div class="text-xs text-gray-600">
          <span v-if="saving">저장중...</span>
          <span v-else-if="saved">저장됨</span>
          <span v-else>수정됨</span>
        </div>
      </div>

      <!-- ✅ 타이틀 옆(오른쪽) 버튼들 -->
      <div class="flex items-center gap-2 shrink-0">
        <div class="">
          <button class="px-2 text-xs input-panel-icon font-bold" @click="$emit('openMyProblemSet')">
            내 문제
          </button>
        </div>
        <div class="">
          <button class="px-2 text-xs input-panel-icon font-bold" @click="$emit('openHistory')">
            히스토리
          </button>
        </div>
        <div class="">
          <button class="px-3.5 text-xs input-panel-icon font-bold" @click="$emit('openBadge')">
            뱃지
          </button>
        </div>
      </div>
    </div>

    <!-- ✅ textarea가 남은 공간 전부 차지 -->
    <div class="flex-1  min-h-0">
      <textarea
        v-model="memo"
        class="h-full w-full p-2 resize-none no-scrollbar
               bg-white/25 text-sm text-black
               border-2 rounded-md border-black/25 outline-none transition-colors
               focus:border-black/50
               placeholder:text-black/40"
        placeholder="여기에 개인 메모를 작성하세요..."
      />
    </div>

    <!-- ✅ 에러는 아래 고정 -->
    <div v-if="error" class="text-red-500 text-xs shrink-0">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { fetchMemo, saveMemo } from "@/api/profile"
import { ref, onMounted, onBeforeUnmount, watch } from "vue"

defineEmits(["openHistory", "openBadge", "openMyProblemSet"])

const memo = ref("")
const saving = ref(false)
const saved = ref(true)
const error = ref("")
let debounceTimer = null


const load = async () => {
  error.value = ""
  try {
    const res = await fetchMemo()
    memo.value = res.data.memo ?? ""
    saved.value = true
  } catch (e) {
    console.error(e)
    error.value = "메모를 불러오지 못했습니다."
  }
}

const save = async () => {
  if (saving.value) return
  saving.value = true
  error.value = ""
  try {
    await saveMemo(memo.value)
    saved.value = true
  } catch (e) {
    console.error(e)
    error.value = "저장에 실패했습니다."
  } finally {
    saving.value = false
  }
}

const manualSave = async () => {
  if (debounceTimer) clearTimeout(debounceTimer)
  await save()
}

const reload = async () => {
  if (debounceTimer) clearTimeout(debounceTimer)
  await load()
}

watch(memo, () => {
  saved.value = false
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => save(), 600)
})

onMounted(load)

onBeforeUnmount(() => {
  if (debounceTimer) clearTimeout(debounceTimer)
})
</script>
