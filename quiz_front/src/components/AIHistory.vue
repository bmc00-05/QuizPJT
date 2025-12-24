<template>
  <!-- ✅ 모바일 프레임 기준: 최대 너비 420px + 뷰포트 높이 제한 -->
  <div class="w-full text-black max-w-[420px] mx-auto">
    <!-- ✅ 헤더(고정) -->
    <div class="flex items-center justify-between mb-2 shrink-0">
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

    <!-- ✅ 컨텐츠 래퍼: 화면 높이에 맞춰 최대 높이 제한 -->
    <div class="rounded border bg-white/60">
      <!-- 로딩/에러 -->
      <div v-if="loading" class="p-3 text-sm text-black/60">불러오는 중...</div>

      <div v-else-if="error" class="p-3 text-sm text-red-600">
        {{ error }}
        <button class="ml-2 underline" @click="fetchHistory">재시도</button>
      </div>

      <!-- ✅ 본문: 스크롤 영역(스크롤바 숨김) -->
      <div
        v-else
        class="
          max-h-[70vh] sm:max-h-[75vh]
          overflow-y-auto
          scrollbar-hide
          p-2
        "
      >
        <!-- ===================== -->
        <!-- ✅ LIST MODE -->
        <!-- ===================== -->
        <div v-if="mode === 'list'">
          <!-- 메타 -->
          <div class="text-xs text-black/50 mb-2 flex items-center gap-2 px-1">
            <span>page: {{ raw?.page ?? '-' }}</span>
            <span>/</span>
            <span>total: {{ raw?.total ?? items.length }}</span>
          </div>

          <!-- 목록 -->
          <div v-if="items.length === 0" class="text-sm text-black/60 p-2">
            히스토리가 없습니다.
          </div>

          <ul v-else class="space-y-2">
            <li
              v-for="item in items"
              :key="item.id"
              class="cursor-pointer rounded border bg-white/70 hover:bg-white p-2"
              @click="openDetail(item)"
            >
              <div class="flex items-center justify-between">
                <div class="text-sm font-bold">#{{ item.id }}</div>
                <div class="text-xs text-black/60">
                  {{ item.created_at }}
                </div>
              </div>

              <div class="text-xs text-black/60 mt-1">
                model: {{ item.model_name }} / wrong: {{ item.wrong_count }} / days: {{ item.days }}
              </div>

              <div class="text-xs mt-2 text-black/80">
                {{ (item.feedback ?? '').slice(0, 120) }}{{ (item.feedback ?? '').length > 120 ? '...' : '' }}
              </div>
            </li>
          </ul>
        </div>

        <!-- ===================== -->
        <!-- ✅ DETAIL MODE (전문) -->
        <!-- ===================== -->
        <div v-else class="p-1">
          <div class="text-xs text-black/60 mb-2">
            {{ selected?.created_at }} / {{ selected?.model_name }} /
            wrong: {{ selected?.wrong_count }} / days: {{ selected?.days }}
          </div>

          <!-- ✅ 전문은 길어질 수 있으니 여기서도 스크롤 가능하게(바 숨김) -->
          <div
            class="
              rounded border bg-white/70 p-2
              max-h-[55vh] sm:max-h-[60vh]
              overflow-y-auto
              scrollbar-hide
              whitespace-pre-wrap
              text-sm
            "
          >
            {{ selected?.feedback }}
          </div>

          <div class="mt-3 flex gap-3">
            <button class="text-sm underline" @click="emitSelect">
              이 코칭을 프로필에 표시
            </button>
            <button class="text-sm underline" @click="backToList">
              목록으로
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import axios from "axios"

const props = defineProps({
  apiUrl: { type: String, required: true },
  token: { type: String, required: true },
  endpoint: { type: String, required: true },
})

const emit = defineEmits(["close", "select"])

const raw = ref(null)
const loading = ref(false)
const error = ref("")

const mode = ref("list") // 'list' | 'detail'
const selected = ref(null)

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
}

const backToList = () => {
  mode.value = "list"
  selected.value = null
}

const emitSelect = () => {
  if (!selected.value) return
  emit("select", selected.value)
}

onMounted(fetchHistory)
</script>

<style scoped>
/* ✅ 스크롤은 되지만 스크롤바는 안 보이게 */
.scrollbar-hide {
  -ms-overflow-style: none; /* IE/Edge */
  scrollbar-width: none; /* Firefox */
}
.scrollbar-hide::-webkit-scrollbar {
  display: none; /* Chrome/Safari */
}
</style>
