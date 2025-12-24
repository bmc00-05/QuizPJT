<template>
  <div class="text-black">
    <!-- 로딩/에러 표시(선택) -->
    <div v-if="loading" class="text-sm text-black/60">불러오는 중...</div>
    <div v-else-if="error" class="text-sm text-red-600">
      {{ error }}
      <button class="ml-2 underline" @click="getStatus">재시도</button>
    </div>

    <div v-else-if="stats">
      <div class=" max-w-[250px] text-sm">
    
          <span class="font-bold flex justify-center">
            LV. {{ stats.profile.level }} {{ stats.profile.username }}
            
          </span>
          <br />

          <span>
            EXP {{ stats.profile.exp }} / {{ stats.profile.max_exp }}
          </span>

          <br />
          <hr />

          <span class="m-1 font-bold flex justify-center">
            통계
          </span>
          푼 문제: {{ stats.stats.total_solved }} <br />
          맞춘 문제: {{ stats.stats.total_correct }} <br />
          정확도: {{ stats.stats.accuracy_pct }} %
          <hr />

          <span class="m-1 font-bold flex justify-center">
            숙련도
          </span>
          <div v-for="category in stats.category_stats" :key="category.category_id">
            <span>{{ category.category_name }}</span>: {{ category.proficiency_score }}
          </div>
        </div>
      </div>


    <div v-else class="text-sm text-black/60">
      표시할 데이터가 없습니다.
    </div>
  </div>
</template>

<script setup>
import { useAccountStore } from "@/stores/accounts"
import axios from "axios"
import { ref, onMounted, watch } from "vue"



// const badge = stats.profile.equipped_badge.icon
const props = defineProps({
  // ✅ 없으면 내 상태, 있으면 해당 유저 상태
  userId: { type: [Number, String], default: null },
})

const accountStore = useAccountStore()
const API_URL = import.meta.env.VITE_REST_API_URL

const stats = ref(null)
const loading = ref(false)
const error = ref("")

const buildUrl = () => {
  // ✅ 여기만 너 urls.py에 맞게 바꾸면 됨
  // 1) 내 상태
  if (!props.userId) return `${API_URL}/profile/status/`

  // 2) 다른 유저 상태(예: /profile/status/7/)
  return `${API_URL}/profile/status/${props.userId}/`
}

const getStatus = async () => {
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

onMounted(getStatus)

// ✅ userId 바뀌면 자동 재조회
watch(() => props.userId, () => {
  getStatus()
})
</script>

<style scoped>
</style>
