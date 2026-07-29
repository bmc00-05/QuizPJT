<template>
  <div class="mx-2">
    <div class="text-black">
      <div class="flex items-center justify-start mb-2">
        <h2 class="font-bold">뱃지 도감</h2>
        <div class="text-xs ml-5 text-gray-600">
          보유: {{ ownedCount }} / {{ badges.length }}
        </div>
      </div>

      <div v-if="loading" class="text-sm text-gray-500">불러오는 중...</div>
      <div v-else-if="error" class="text-sm text-red-600">{{ error }}</div>

      <div v-else class="grid grid-cols-4 gap-2">
        <button
          v-for="b in badges"
          :key="b.id"
          class="relative aspect-square border rounded overflow-hidden hover:scale-[0.99]"
          :class="[
            b.owned ? 'bg-white' : 'bg-gray-100 opacity-60',
            b.equipped ? 'ring-2 ring-yellow-400' : '',
            selectedId === b.id ? 'outline outline-2 outline-blue-400' : '',
          ]"
          :aria-label="b.name"
          @click="select(b)"
        >
          <img
            v-if="b.icon"
            :src="b.icon"
            class="w-full h-full object-contain p-1 [image-rendering:pixelated]"
            :class="!b.owned ? 'grayscale' : ''"
            alt=""
          />
          <div
            v-else
            class="w-full h-full flex items-center justify-center text-[10px] text-gray-600"
          >
            NO ICON
          </div>

          <span
            v-if="b.equipped"
            class="absolute top-1 left-1 text-[10px] px-1 bg-yellow-300 rounded"
          >
            E
          </span>
          <span
            v-if="!b.owned"
            class="absolute bottom-1 left-1 text-[10px] px-1 bg-black/60 text-white rounded"
          >
            LOCK
          </span>
        </button>
      </div>

      <div class="mt-3 border-t pt-3">
        <div v-if="selected">
          <div class="flex items-center gap-2">
            <div class="font-bold">{{ selected.name }}</div>
            <span
              v-if="!selected.owned"
              class="text-[10px] px-1 py-0.5 bg-gray-200 text-gray-600 rounded"
            >
              미보유
            </span>
          </div>

          <div class="text-xs text-gray-700 mt-1">{{ selected.description }}</div>

          <div class="text-xs text-gray-500 mt-1" v-if="selected.earned_at">
            획득: {{ formatDate(selected.earned_at) }}
          </div>

          <!-- 미보유 뱃지는 설명만 보여주고 착용 버튼을 노출하지 않는다 -->
          <div v-if="!selected.owned" class="mt-3 text-xs text-gray-500">
            아직 획득하지 않은 뱃지입니다.
          </div>

          <div v-else class="mt-3 flex gap-2">
            <button
              class="button-green px-1"
              :disabled="selected.equipped || equipping"
              @click="equipSelected"
            >
              {{ selected.equipped ? "착용중" : (equipping ? "착용중..." : "착용하기") }}
            </button>

            <button
              class="button-red px-2"
              :disabled="equipping"
              @click="unequip"
            >
              해제
            </button>
          </div>
        </div>

        <div v-else class="text-sm text-gray-500">
          뱃지를 선택하면 설명이 표시됩니다.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { fetchBadges, equipBadge, unequipBadge } from "@/api/profile"
import { useDialogStore } from "@/stores/dialog"

const dialog = useDialogStore()

const badges = ref([])
const loading = ref(false)
const error = ref("")

const selectedId = ref(null)
const selected = computed(() => badges.value.find((b) => b.id === selectedId.value) ?? null)

const equipping = ref(false)
const ownedCount = computed(() => badges.value.filter((b) => b.owned).length)

/**
 * ✅ 확장자 대문자(.PNG)까지 잡으려고 *.* 사용
 * (기존 *.{png,...}는 .PNG면 매칭 안 됨)
 */
const badgeModules = import.meta.glob("/src/assets/badges/*.*", {
  eager: true,
  import: "default",
})

/**
 * ✅ 파일 base name을 무조건 소문자로 key화
 * - /src/assets/badges/WELCOME_HOME.PNG => key "welcome_home"
 */
const ICON_BY_CODE = (() => {
  const map = {}
  for (const [path, url] of Object.entries(badgeModules)) {
    const filename = path.split("/").pop() || ""
    const base = filename.replace(/\.[^/.]+$/, "")
    map[base.toLowerCase()] = url
  }
  return map
})()

/**
 * ✅ 현재 네 프로젝트 로컬 파일명에 맞추는 alias
 * (원하면 나중에 파일명/code 통일하면 이거 삭제하면 됨)
 */
const CODE_ALIAS = {
  welcome: "welcome_home",
  badge_1: "cat_base",
  badge_2: "unnamed",
  // default, first_clear, level_10은 파일만 있으면 그대로 매칭됨
}

const normalizeKey = (code) => {
  return String(code || "")
    .trim()
    .toLowerCase()
    .replace(/\s+/g, "_")
    .replace(/-/g, "_")
}

const resolveBadgeIcon = (code) => {
  const normalized = normalizeKey(code)
  const aliased = CODE_ALIAS[normalized] || normalized
  return ICON_BY_CODE[aliased] || ICON_BY_CODE["default"] || null
}

const fetchDex = async () => {
  loading.value = true
  error.value = ""
  try {
    const res = await fetchBadges()

    badges.value = (res.data ?? []).map((b) => {
      const localIcon = resolveBadgeIcon(b.code)
      return {
        ...b,
        icon: localIcon || null, // ✅ 로컬로 고정 (DB icon 혼선 제거)
      }
    })

    const equipped = badges.value.find((b) => b.equipped)
    if (equipped) selectedId.value = equipped.id
  } catch (e) {
    error.value = e?.response?.data?.detail || "뱃지를 불러오지 못했습니다."
  } finally {
    loading.value = false
  }
}

/**
 * 미보유 뱃지도 선택할 수 있다.
 * 도감이므로 어떤 뱃지가 있는지 미리 볼 수 있어야 하고,
 * 착용만 막으면 충분하다.
 */
const select = (b) => {
  selectedId.value = b.id
}

const equipSelected = async () => {
  if (!selected.value) return
  equipping.value = true
  try {
    await equipBadge(selected.value.id)
    await fetchDex()
  } catch (e) {
    dialog.alert(e?.response?.data?.detail || "착용 실패", { tone: "danger" })
  } finally {
    equipping.value = false
  }
}

const unequip = async () => {
  equipping.value = true
  try {
    await unequipBadge()
    await fetchDex()
  } catch (e) {
    dialog.alert(e?.response?.data?.detail || "해제 실패", { tone: "danger" })
  } finally {
    equipping.value = false
  }
}

const formatDate = (iso) => {
  try {
    return new Date(iso).toLocaleString()
  } catch {
    return iso
  }
}

onMounted(fetchDex)
</script>