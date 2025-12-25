<template>
  <div class="w-full h-full min-h-0 text-black">
    <!-- 로딩/에러 -->
    <div v-if="loading" class="text-[11px] opacity-70 p-2">불러오는 중...</div>
    <div v-else-if="error" class="text-[11px] text-red-600 p-2">
      {{ error }}
      <button class="ml-2 underline" @click="getStatus">재시도</button>
    </div>

    <div v-else-if="stats" class="w-full h-full min-h-0 p-2 flex flex-col gap-2">
      <!-- ✅ 탭(반으로 분할) -->
      <div class="flex gap-1">
        <button
          type="button"
          class="flex-1 py-1 text-[11px] border border-black/30 bg-black/5"
          :class="activeTab === 'status' ? 'bg-black/15 font-bold' : 'opacity-70'"
          @click="activeTab = 'status'"
        >
          스테이터스
        </button>

        <button
          type="button"
          class="flex-1 py-1 text-[11px] border border-black/30 bg-black/5"
          :class="activeTab === 'mastery' ? 'bg-black/15 font-bold' : 'opacity-70'"
          @click="activeTab = 'mastery'"
        >
          숙련도
        </button>
      </div>

      <!-- ✅ 내용 영역(항상 스크롤로 안정화) -->
      <div class="flex-1 min-h-0 overflow-y-auto no-scrollbar pr-0.5">
        <!-- =======================
             스테이터스 탭
        ======================== -->
        <div v-if="activeTab === 'status'" class="flex flex-col gap-2" @click="activeTab='mastery'">
          <!-- 1) 헤더 + EXP -->
          <div class="flex flex-col gap-1">
            <div class="flex items-baseline justify-between gap-2">
              <div class="min-w-0 font-bold text-[13px] leading-tight truncate">
                Lv.{{ stats.profile.level }} {{ stats.profile.username }}
              </div>
              <div class="shrink-0 text-[10px] opacity-80">
                {{ expPct }}%
              </div>
            </div>

            <div class="text-[11px] leading-tight opacity-90">
              EXP {{ stats.profile.exp }} / {{ stats.profile.max_exp }}
            </div>

            <div class="w-full mt-1">
              <div class="h-2 border border-black/40 bg-black/5">
                <div class="h-full bg-black/60" :style="{ width: expPct + '%' }" />
              </div>
            </div>
          </div>

          <hr class="border-black/30" />

          <!-- 2) 통계 (✅ 반응형 제거: 고정 2열 + 마지막은 2칸) -->
          <div>
            <div class="font-bold text-[12px] mb-1">통계</div>
            <div class="grid grid-cols-2 gap-1">
              <div class="border border-black/20 bg-black/5 px-2 py-1">
                <div class="text-[10px] opacity-80">품</div>
                <div class="font-bold text-[12px] leading-tight">
                  {{ stats.stats.total_solved }}
                </div>
              </div>

              <div class="border border-black/20 bg-black/5 px-2 py-1">
                <div class="text-[10px] opacity-80">맞춤</div>
                <div class="font-bold text-[12px] leading-tight">
                  {{ stats.stats.total_correct }}
                </div>
              </div>

              <div class="border border-black/20 bg-black/5 px-2 py-1 col-span-2">
                <div class="text-[10px] opacity-80">정확도</div>
                <div class="font-bold text-[12px] leading-tight">
                  {{ stats.stats.accuracy_pct }}%
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- =======================
             숙련도 탭
        ======================== -->
        <div v-else class="flex flex-col gap-2" @click="activeTab='status'">
          <div class="font-bold text-[12px]">숙련도</div>

          <div v-if="(stats.category_stats?.length ?? 0) === 0" class="text-[11px] opacity-70" > 
            표시할 숙련도 데이터가 없습니다.
          </div>

          <!-- ✅ 반응형 제거: 항상 1열 -->
          <div v-else class="grid grid-cols-1 gap-y-2">
            <div
              v-for="c in stats.category_stats"
              :key="c.category_id"
              class="min-w-0"
            >
              <div class="flex items-center justify-between gap-2">
                <span class="text-[11px] truncate">{{ c.category_name }}</span>
                <span class="text-[11px] font-bold tabular-nums">
                  {{ Number(c.proficiency_score).toFixed(1) }}
                </span>
              </div>

              <div class="h-1.5 border border-black/20 bg-black/5">
                <div
                  class="h-full bg-black/60"
                  :style="{ width: profPct(c.proficiency_score) + '%' }"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-[11px] opacity-70 p-2">표시할 데이터가 없습니다.</div>
  </div>
</template>

<script setup>
import { useAccountStore } from "@/stores/accounts"
import axios from "axios"
import { ref, watch, computed } from "vue"

const props = defineProps({
  userId: { type: [Number, String], default: null },
})

const accountStore = useAccountStore()
const API_URL = import.meta.env.VITE_REST_API_URL

const stats = ref(null)
const loading = ref(false)
const error = ref("")

// ✅ 탭 상태
const activeTab = ref("status") // 'status' | 'mastery'

const buildUrl = () => {
  if (!props.userId) return `${API_URL}/profile/status/`
  return `${API_URL}/profile/status/${props.userId}/`
}

const getStatus = async () => {
  if (!accountStore.token) return

  loading.value = true
  error.value = ""
  try {
    const res = await axios.get(buildUrl(), {
      headers: { Authorization: `Token ${accountStore.token}` },
    })
    stats.value = res.data
  } catch (e) {
    console.error(e)
    stats.value = null
    error.value = e?.response?.data?.detail || "상태 정보를 불러오지 못했습니다."
  } finally {
    loading.value = false
  }
}

// ✅ EXP 퍼센트
const expPct = computed(() => {
  const exp = Number(stats.value?.profile?.exp ?? 0)
  const max = Math.max(1, Number(stats.value?.profile?.max_exp ?? 1))
  return Math.min(100, Math.round((exp / max) * 100))
})

// ✅ 숙련도 바 퍼센트
const PROF_MAX = 100
const profPct = (score) => {
  const v = Number(score ?? 0)
  return Math.min(100, Math.max(0, Math.round((v / PROF_MAX) * 100)))
}

// ✅ 토큰 준비되면 자동 로딩 + userId 바뀌면 재조회
watch(
  () => [accountStore.token, props.userId],
  ([token]) => {
    if (token) getStatus()
  },
  { immediate: true }
)
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
