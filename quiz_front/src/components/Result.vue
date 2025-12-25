<template>
  <div class="w-full text-black">
    <div class=" w-[92vw] max-w-[300px]">
      <div class="p-3 flex flex-col gap-3">

        <!-- 1) 타이틀 -->
        <div class="text-center">
          <div class="text-xl font-black tracking-widest">RESULT</div>
          <div v-if="levelUp" class="text-[11px] font-bold mt-1">
            LEVEL UP!
          </div>
        </div>

        <!-- 2) 요약 3칸 -->
        <div class="grid grid-cols-3 gap-2">
          <div class="input-panel-icon px-2 py-2 text-center">
            <div class="text-[10px] opacity-70">정답</div>
            <div class="text-[14px] font-black tabular-nums">{{ r.correct }}</div>
          </div>

          <div class="input-panel-icon px-2 py-2 text-center">
            <div class="text-[10px] opacity-70">총 문제</div>
            <div class="text-[14px] font-black tabular-nums">{{ r.total }}</div>
          </div>

          <div class="input-panel-icon px-2 py-2 text-center">
            <div class="text-[10px] opacity-70">정확도</div>
            <div class="text-[14px] font-black tabular-nums">{{ accuracy }}%</div>
          </div>
        </div>

        <!-- 3) 레벨 변화 -->
        <div class="input-panel-icon px-2 py-2">
          <div class="flex items-center justify-between text-[11px]">
            <span class="opacity-70">레벨</span>
            <span class="font-bold tabular-nums">
              {{ r.level_before }} → {{ r.level_after }}
            </span>
          </div>
          <div class="flex items-center justify-between text-[11px] mt-1">
            <span class="opacity-70">획득 경험치</span>
            <span class="font-bold tabular-nums">+{{ r.score }}</span>
          </div>
        </div>

        <!-- ✅ 4) EXP 게이지 (요청대로 "아래쪽"으로 내림) -->
        <div class="input-panel-icon px-2 py-2">
          <div class="flex items-center justify-between text-[11px] opacity-90">
            <span>EXP</span>
            <span class="text-[10px] tabular-nums opacity-80">{{ expPct }}%</span>
          </div>

          <div class="mt-2 h-2 border border-black/40 bg-black/5 overflow-hidden">
            <div
              class="h-full bg-black/60 transition-[width] duration-500"
              :style="{ width: expPct + '%' }"
            />
          </div>

          <div class="mt-1 text-[10px] opacity-80 tabular-nums">
            {{ expNow }} / {{ expMax }}
          </div>
        </div>

        <!-- 5) 버튼 -->
        <div class="flex gap-2">
          <button type="button" class="button-panel flex-1" @click="$emit('goMap')">
            <div class="pixel-panel__content p-2 text-center font-bold">맵으로</div>
          </button>
          <button type="button" class="button-panel flex-1" @click="$emit('close')">
            <div class="pixel-panel__content p-2 text-center font-bold">닫기</div>
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  // session_result 그대로 받기
  result: { type: Object, required: true },
  // exp 표시용(없어도 동작)
  expNow: { type: Number, default: 0 },
  expMax: { type: Number, default: 100 },
})

defineEmits(["close", "goMap"])

const r = computed(() => props.result ?? {})

const accuracy = computed(() => {
  const total = Number(r.value.total ?? 0)
  const correct = Number(r.value.correct ?? 0)
  if (!total) return 0
  return Math.round((correct / total) * 100)
})

const levelUp = computed(() => {
  return Number(r.value.level_after ?? 0) > Number(r.value.level_before ?? 0)
})

const expPct = computed(() => {
  const max = Math.max(1, Number(props.expMax))
  const now = Math.max(0, Number(props.expNow))
  return Math.min(100, Math.round((now / max) * 100))
})
</script>