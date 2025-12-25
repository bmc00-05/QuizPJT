<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center">
    <!-- backdrop -->
    <div class="absolute inset-0 bg-black/60" @click="onClose" />

    <!-- modal -->
    <div class="relative z-10 w-[calc(100%-2rem)] max-w-[360px] pixel-panel overflow-hidden">
      <div class="p-4 flex flex-col gap-3">
        <div class="text-[13px] font-bold">🎉 뱃지 획득!</div>

        <div v-if="current" class="flex gap-3 items-center">
          <img
            v-if="current.icon"
            :src="current.icon"
            class="w-14 h-14 [image-rendering:pixelated]"
            alt="badge"
          />
          <div class="min-w-0">
            <div class="text-[12px] font-bold truncate">{{ current.name }}</div>
            <div class="text-[11px] opacity-80 break-words">
              {{ current.description }}
            </div>
          </div>
        </div>

        <div class="text-[11px] opacity-60">
          {{ index + 1 }} / {{ badges.length }}
        </div>

        <div class="flex justify-end gap-2">
          <button class="text-xs input-panel-icon px-2 py-1" @click="next">
            {{ isLast ? "닫기" : "다음" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"

const props = defineProps({
  badges: { type: Array, default: () => [] },
})
const emit = defineEmits(["close"])

const index = ref(0)

const current = computed(() => props.badges[index.value] ?? null)
const isLast = computed(() => index.value >= props.badges.length - 1)

function next() {
  if (isLast.value) onClose()
  else index.value += 1
}

function onClose() {
  emit("close")
}
</script>