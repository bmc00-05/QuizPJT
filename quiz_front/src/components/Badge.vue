<template>
  <div class=" mx-2">
    <div class=" text-black">
      <div class="flex items-center justify-between mb-2">
        <h2 class="font-bold">뱃지 도감</h2>
        <div class="text-xs text-gray-600">
          보유: {{ ownedCount }} / {{ badges.length }}
        </div>
      </div>

      <div v-if="loading" class="text-sm text-gray-500">불러오는 중...</div>
      <div v-else-if="error" class="text-sm text-red-600">{{ error }}</div>

      <!-- ✅ 도감 그리드 -->
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
            class="w-full h-full object-contain p-1"
            :class="!b.owned ? 'grayscale' : ''"
            alt=""
          />
          <div v-else class="w-full h-full flex items-center justify-center text-[10px] text-gray-600">
            NO ICON
          </div>

          <span v-if="b.equipped" class="absolute top-1 left-1 text-[10px] px-1 bg-yellow-300 rounded">
            E
          </span>
          <span v-if="!b.owned" class="absolute bottom-1 left-1 text-[10px] px-1 bg-black/60 text-white rounded">
            LOCK
          </span>
        </button>
      </div>

      <!-- ✅ 선택된 뱃지 설명 -->
      <div class="mt-3 border-t pt-3">
        <div v-if="selected">
          <div class="font-bold">{{ selected.name }}</div>
          <div class="text-xs text-gray-700 mt-1">{{ selected.description }}</div>
          <div class="text-xs text-gray-500 mt-1" v-if="selected.earned_at">
            획득: {{ formatDate(selected.earned_at) }}
          </div>

          <div class="mt-3 flex gap-2">
            <button
              class="px-3 py-2 border rounded bg-white hover:bg-gray-50"
              :disabled="selected.equipped || equipping"
              @click="equipSelected"
            >
              {{ selected.equipped ? '착용중' : (equipping ? '착용중...' : '착용하기') }}
            </button>

            <button
              class="px-3 py-2 border rounded bg-white hover:bg-gray-50"
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
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()

const badges = ref([])
const loading = ref(false)
const error = ref('')

const selectedId = ref(null)
const selected = computed(() => badges.value.find(b => b.id === selectedId.value) ?? null)

const equipping = ref(false)

const ownedCount = computed(() => badges.value.filter(b => b.owned).length)

const fetchDex = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_URL}/profile/badges/`, {
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    badges.value = res.data
    // 기본 선택: 착용중이면 그걸 선택
    const equipped = badges.value.find(b => b.equipped)
    if (equipped) selectedId.value = equipped.id
  } catch (e) {
    error.value = e?.response?.data?.detail || '뱃지를 불러오지 못했습니다.'
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
    await axios.post(`${API_URL}/profile/equip-badge/`,
      { badge_id: selected.value.id },
      { headers: { Authorization: `Token ${accountStore.token}` } }
    )
    await fetchDex() // 착용 표시 갱신
  } catch (e) {
    alert(e?.response?.data?.detail || '착용 실패')
  } finally {
    equipping.value = false
  }
}

const unequip = async () => {
  equipping.value = true
  try {
    await axios.post(`${API_URL}/profile/unequip-badge/`, {},
      { headers: { Authorization: `Token ${accountStore.token}` } }
    )
    await fetchDex()
  } catch (e) {
    alert(e?.response?.data?.detail || '해제 실패')
  } finally {
    equipping.value = false
  }
}

const formatDate = (iso) => {
  try { return new Date(iso).toLocaleString() } catch { return iso }
}

onMounted(fetchDex)
</script>
