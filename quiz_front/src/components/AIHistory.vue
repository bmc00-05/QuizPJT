<template>
  <div class="w-full min-h-0 flex flex-col text-black">
    <!-- 헤더(고정) -->
    <header class="shrink-0">
      <div class="flex items-center justify-between mb-2">
        <div class="flex items-center gap-2">
          <button
            v-if="mode === 'detail'"
            class="text-sm underline"
            @click="backToList"
          >
            ← 목록
          </button>

          <h2 class="text-lg font-bold">
            {{ mode === 'list' ? 'AI 코칭 히스토리' : `코칭 #${selected?.id}` }}
          </h2>
        </div>
      </div>
    </header>

    <!-- 가운데만 스크롤 -->
    <main class="flex-1 min-h-0 overflow-y-auto no-scrollbar pr-1">
      <!-- 로딩/에러 -->
      <div v-if="loading" class="p-2 text-sm text-black/60">
        불러오는 중...
      </div>

      <div v-else-if="error" class="p-2 text-sm text-red-600">
        {{ error }}
        <button class="ml-2 underline" @click="fetchHistory">재시도</button>
      </div>

      <!-- 본문 -->
      <div v-else>
        <!-- LIST -->
        <div v-if="mode === 'list'">
          <div class="text-xs text-black/50 mb-2 flex items-center gap-2 px-1">
            <span>page: {{ raw?.page ?? '-' }}</span>
            <span>/</span>
            <span>total: {{ raw?.total ?? items.length }}</span>
          </div>

          <ul v-if="items.length" class="flex flex-col gap-2">
            <li v-for="item in items" :key="item.id">
              <button
                type="button"
                class="w-full input-panel-icon px-3 py-2 text-left transition-transform active:scale-[0.99]"
                @click="openDetail(item)"
              >
                <div class="flex items-center justify-between gap-2">
                  <div class="min-w-0">
                    <div class="font-semibold text-[13px] leading-snug">
                      코칭 #{{ item.id }}
                    </div>
                    <div class="text-[11px] opacity-70 mt-0.5 truncate">
                      {{ item.created_at }} / {{ item.model_name }}
                    </div>
                    <div class="text-[11px] opacity-70 mt-0.5">
                      wrong {{ item.wrong_count }} / days {{ item.days }}
                    </div>
                    <div class="text-[11px] mt-1 opacity-80">
                      {{ (item.feedback ?? "").slice(0, 90) }}{{ (item.feedback ?? "").length > 90 ? "..." : "" }}
                    </div>
                  </div>

                  <span class="text-[11px] opacity-70 shrink-0">▶</span>
                </div>
              </button>
            </li>
          </ul>

          <div v-else class="text-sm text-black/60 p-2">
            히스토리가 없습니다.
          </div>
        </div>

        <!-- DETAIL -->
        <div v-else>
          <div class="text-xs text-black/60 mb-2">
            {{ selected?.created_at }} / {{ selected?.model_name }} /
            wrong {{ selected?.wrong_count }} / days {{ selected?.days }}
          </div>

          <div class="rounded p-3 input-panel-icon text-sm">
            {{ selected?.feedback }}
          </div>

          <div v-if="deleteError" class="mt-2 text-xs text-red-600">
            {{ deleteError }}
          </div>
        </div>
      </div>
    </main>

    <!-- 하단 버튼(고정) -->
    <footer class="shrink-0 pt-3">
      <!-- LIST MODE 버튼 -->
      <div v-if="mode === 'list'" class="flex justify-center gap-2">
        <button
          type="button"
          class="button-panel w-full max-w-[160px]"
          :disabled="loading"
          @click="fetchHistory"
        >
          <div class="pixel-panel__content p-2 text-center font-bold">
            {{ loading ? "불러오는 중..." : "새로고침" }}
          </div>
        </button>

        <button
          type="button"
          class="button-panel w-full max-w-[120px]"
          @click="emitClose"
        >
          <div class="pixel-panel__content p-2 text-center font-bold">닫기</div>
        </button>
      </div>

      <!-- DETAIL MODE 버튼: [삭제][목록][닫기] -->
      <div v-else class="grid grid-cols-3 gap-2 items-center">
        <button
          type="button"
          class="button-panel w-full"
          :disabled="deleting"
          @click="deleteSelected"
        >
          <div class="pixel-panel__content p-2 text-center font-bold">
            {{ deleting ? "삭제중..." : "삭제" }}
          </div>
        </button>

        <button
          type="button"
          class="button-panel w-full"
          :disabled="deleting"
          @click="backToList"
        >
          <div class="pixel-panel__content p-2 text-center font-bold">목록</div>
        </button>

        <button
          type="button"
          class="button-panel w-full"
          :disabled="deleting"
          @click="emitClose"
        >
          <div class="pixel-panel__content p-2 text-center font-bold">닫기</div>
        </button>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import axios from "axios"

const props = defineProps({
  apiUrl: { type: String, required: true },
  token: { type: String, required: true },
  endpoint: { type: String, required: true }, // list/history endpoint
})

const emit = defineEmits(["close", "select"])
const emitClose = () => emit("close")

const raw = ref(null)
const loading = ref(false)
const error = ref("")

const mode = ref("list")
const selected = ref(null)

const deleting = ref(false)
const deleteError = ref("")

const items = computed(() => {
  const d = raw.value
  return Array.isArray(d?.items) ? d.items : []
})

const fetchHistory = async () => {
  loading.value = true
  error.value = ""
  try {
    const res = await axios.get(`${props.apiUrl}${props.endpoint}`, {
      headers: { Authorization: `Token ${props.token}` },
    })
    raw.value = res.data
  } catch (e) {
    console.error(e)
    error.value = e?.response?.data?.detail || "히스토리를 불러오지 못했습니다."
  } finally {
    loading.value = false
  }
}

const openDetail = (item) => {
  selected.value = item
  mode.value = "detail"
  deleteError.value = ""
}

const backToList = () => {
  mode.value = "list"
  selected.value = null
  deleteError.value = ""
}

/**
 * ✅ 삭제 URL 빌더
 * - 여기만 네 API에 맞게 바꿔서 쓰면 됨.
 */
const buildDeleteUrl = (id) => {
  // TODO: 네 서버 삭제 URL로 교체
  // 예) return `${props.apiUrl}/ai/feedback/history/${id}/`
  return `${props.apiUrl}/ai/feedback/history/${id}/delete/`
}

const removeFromList = (id) => {
  if (!raw.value || !Array.isArray(raw.value.items)) return
  raw.value.items = raw.value.items.filter((x) => x.id !== id)

  // total 같은 메타가 있으면 같이 조정(선택)
  if (typeof raw.value.total === "number") {
    raw.value.total = Math.max(0, raw.value.total - 1)
  }
}

const deleteSelected = async () => {
  if (!selected.value?.id) return
  if (deleting.value) return

  const ok = window.confirm("이 히스토리를 삭제할까요?")
  if (!ok) return

  deleting.value = true
  deleteError.value = ""

  try {
    const url = buildDeleteUrl(selected.value.id)
    await axios.delete(url, {
      headers: { Authorization: `Token ${props.token}` },
    })

    // ✅ 삭제 성공: 리스트에서 제거 + 목록으로 복귀
    removeFromList(selected.value.id)
    backToList()
  } catch (e) {
    console.error(e)
    deleteError.value = e?.response?.data?.detail || "삭제에 실패했습니다."
  } finally {
    deleting.value = false
  }
}

onMounted(fetchHistory)
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>