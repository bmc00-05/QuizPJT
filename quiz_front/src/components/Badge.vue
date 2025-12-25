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
          class="relative aspect-square border rounded overflow-hidden"
          :class="[
            b.owned ? 'bg-white' : 'bg-gray-100',
            b.equipped ? 'ring-2 ring-yellow-400' : '',
            selectedId === b.id ? 'outline outline-2 outline-blue-400' : '',
            !b.owned ? 'opacity-50 cursor-not-allowed' : 'hover:scale-[0.99]'
          ]"
          :disabled="!b.owned"
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
          <div class="font-bold">{{ selected.name }}</div>
          <div class="text-xs text-gray-700 mt-1">{{ selected.description }}</div>
          <div class="text-xs text-gray-500 mt-1" v-if="selected.earned_at">
            획득: {{ formatDate(selected.earned_at) }}
          </div>

          <div class="mt-3 flex gap-2">
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
          보유한 뱃지를 선택하면 설명과 착용 버튼이 표시됩니다.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import axios from "axios"
import { useAccountStore } from "@/stores/accounts"

const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()

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
    const res = await axios.get(`${API_URL}/profile/badges/`, {
      headers: { Authorization: `Token ${accountStore.token}` },
    })

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

const select = (b) => {
  if (!b.owned) return
  selectedId.value = b.id
}

const equipSelected = async () => {
  if (!selected.value) return
  equipping.value = true
  try {
    await axios.post(
      `${API_URL}/profile/equip-badge/`,
      { badge_id: selected.value.id },
      { headers: { Authorization: `Token ${accountStore.token}` } }
    )
    await fetchDex()
  } catch (e) {
    alert(e?.response?.data?.detail || "착용 실패")
  } finally {
    equipping.value = false
  }
}

const unequip = async () => {
  equipping.value = true
  try {
    await axios.post(
      `${API_URL}/profile/unequip-badge/`,
      {},
      { headers: { Authorization: `Token ${accountStore.token}` } }
    )
    await fetchDex()
  } catch (e) {
    alert(e?.response?.data?.detail || "해제 실패")
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