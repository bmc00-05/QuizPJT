<template>
  <div class="h-full w-full min-h-0 flex flex-col text-black gap-2">
    <!-- 위 패널 -->
    <div class="pixel-panel flex-[11] min-h-0">
      <div
        ref="viewportRef"
        class="relative w-full h-full p-0
              pixel-panel__content
              overflow-hidden select-none touch-none
              flex items-center justify-center"
        @pointerdown="onPointerDown"
        @pointermove="onPointerMove"
        @pointerup="onPointerUp"
        @pointercancel="onPointerUp"
        @wheel.prevent="onWheel"
      >
        <!-- ✅ viewport 안에서 비율 유지: aspect box -->
        <div class="relative w-full h-full">
          <div class="absolute inset-0 will-change-transform" :style="mapTransformStyle">
            <div
              class="absolute inset-0 bg-center bg-cover"
              :style="{ backgroundImage: `url(${mapBgUrl})` }"
            />
            <div class="absolute inset-0 bg-black/20" />

            <button
              v-for="(map, idx) in maps"
              :key="map.id"
              class="absolute px-3 py-2 min-w-[90px]
                    bg-white/80 hover:bg-white
                    border border-gray-400 rounded
                    text-sm font-semibold shadow"
              :style="pinStyle(idx)"
              @click.stop="selectMap(map)"
              @pointerdown.stop
            >
              {{ map.name }}
            </button>
          </div>
        </div>

        <div class="absolute top-2 left-2 z-20 flex gap-2">
          <button class="px-2 py-1 text-xs bg-white/80 border rounded" @click.stop="resetView">
            Reset
          </button>
          <div class="px-2 py-1 text-xs bg-white/80 border rounded">
            x{{ scale.toFixed(2) }}
          </div>
        </div>
      </div>
    </div>
<!-- 아래 패널 (스크롤 버전) -->
<div class="pixel-panel flex-[9] min-h-0">
  <div class="pixel-panel__content p-3 h-full min-h-0 flex flex-col">

    <!-- ✅ 본문만 스크롤 -->
    <div class="flex-1 min-h-0 overflow-auto">
      <template v-if="mapData">


        <div class="grid grid-cols-3 gap-2">
          <!-- 왼쪽(2칸) -->
          <div class="col-span-2 min-w-0">
                    <div class="text-lg font-bold">
          {{ mapData.name }}                         
          <span v-if="problemSetData" class="mt-2 text-sm text-gray-800">
              {{ problemSetData.title }}  
          </span>
          <p class="text-xs font-normal"> {{ mapData.description }} </p>
        </div>
            <div class="w-50 h-28 bg-black/10 rounded mb-2"></div>



            <p v-if="problemSetData">{{ problemSetData.description }}</p>
          </div>

          <!-- 오른쪽(1칸) -->
          <div class="col-span-1 flex flex-col items-end">
            
<button
  :class="[
    activeBtn === 'easy' ? 'button-panel_click' : 'button-panel',
    'w-full max-w-[100px]'
  ]"
  @click="selectProblemSet('easy'); setActiveBtn('easy')"
>
  <div class="pixel-panel__content p-2 font-bold">EASY</div>
</button>

<button
  :class="[
    activeBtn === 'normal' ? 'button-panel_click' : 'button-panel',
    'w-full max-w-[100px]'
  ]"
  @click="selectProblemSet('normal'); setActiveBtn('normal')"
>
  <div class="pixel-panel__content p-2 font-bold">NORMAL</div>
</button>

<button
  :class="[
    activeBtn === 'hard' ? 'button-panel_click' : 'button-panel',
    'w-full max-w-[100px]'
  ]"
  @click="selectProblemSet('hard'); setActiveBtn('hard')"
>
  <div class="pixel-panel__content p-2 font-bold">HARD</div>
</button>

<button
  v-if="problemSetData"
  :class="[
    activeBtn === 'go' ? 'button-panel_click' : 'button-panel',
    'w-full max-w-[100px]'
  ]"
  @click="openModal(); setActiveBtn('go')"
>
  <div class="pixel-panel__content p-2 font-bold">GO!</div>
</button>

          </div>
        </div>
      </template>

      <template v-else>
        <div class="text-sm text-gray-500">
          위 지도에서 맵을 선택하면 정보가 표시됩니다.
        </div>
      </template>
    </div>

    <!-- ✅ 안내문은 고정(스크롤 안 됨) -->
    <div v-if="mapData && !problemSetData" class="shrink-0 pt-2 text-sm text-gray-500">
      난이도를 선택하면 Start가 활성화됩니다.
    </div>

  </div>
</div>

    

    <BaseModal v-if="modal.isOpen && problemSetData" @close="closeModal">
      <div class="text-black">
        모달
        {{ problemSetData.title }} <br/>
        {{ problemSetData.description }}<br/>
        <RouterLink
          :to="{ name: 'game', params: { id: problemSetData.id } }"
          @click="closeModal"
        >
          START
        </RouterLink>
      </div>
    </BaseModal>
  </div>

</template>



<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { useModalStore } from '@/stores/modal'
import { useRoute } from 'vue-router'
import axios from 'axios'
import mapBgUrl from '@/assets/background/game_map.png'
import BaseModal from '@/components/common/BaseModal.vue'

const API_URL = import.meta.env.VITE_REST_API_URL
const modal = useModalStore()
const accountStore = useAccountStore()
const maps = ref([])

const problemSets = ref([])

const mapData = ref(null)
const problemSetData = ref(null)
const isLoadingSets = ref(false)   
const setsError = ref('')          

const route = useRoute()

watch(
  () => route.fullPath,
  () => {
    modal.close() // modal.isOpen=false
  }
)


const activeBtn = ref(null) // 'easy' | 'normal' | 'hard' | 'go'

const setActiveBtn = (key) => {
  activeBtn.value = key
}

const openModal = () => {
  modal.open(1)
}

const closeModal = () => { modal.close() }


const selectMap = async (map) => {
  mapData.value = map
  problemSetData.value = null
  activeBtn.value = null 
  await getProblemSets(map.id)
}

const selectProblemSet = (difficulty) => {
  // difficulty: 'easy' | 'normal' | 'hard'
  const idxMap = { easy: 0, normal: 1, hard: 2 }
  const idx = idxMap[difficulty]

  const picked = problemSets.value?.[idx] ?? null
  problemSetData.value = picked
}

const getProblemSets = async (mapId) => {
  isLoadingSets.value = true
  setsError.value = ''
  problemSets.value = []

  try {
    // ✅ 네 백엔드 map_detail: path('maps/<int:map_pk>/', views.map_detail)
    const res = await axios.get(`${API_URL}/game/maps/${mapId}/`, {
      headers: { Authorization: `Token ${accountStore.token}` },
    })

    // 서버 응답 구조에 따라 아래 둘 중 하나로 맞춰
    // 1) MapProblemSetSerializer가 { id, name, description, problem_sets: [...] } 형태라면:
    problemSets.value = res.data.problem_sets ?? []

    // (선택) mapData도 서버 데이터로 갱신하고 싶다면
    // mapData.value = res.data

  } catch (err) {
    console.error(err)
    setsError.value = '문제집 정보를 불러오지 못했습니다.'
  } finally {
    isLoadingSets.value = false
  }
}


const viewportRef = ref(null)

// ✅ 카메라 상태
const scale = ref(1)
const minScale = 1
const maxScale = 2.5

// translate(px) — “지도 레이어를 얼마나 밀었는지”
const tx = ref(0)
const ty = ref(0)

// 드래그 상태
const dragging = ref(false)
const last = ref({ x: 0, y: 0 })

const mapTransformStyle = computed(() => ({
  transform: `translate(${tx.value}px, ${ty.value}px) scale(${scale.value})`,
  transformOrigin: '0 0',
}))

const getMaps = async () => {
  const res = await axios.get(`${API_URL}/game/maps/`, {
    headers: { Authorization: `Token ${accountStore.token}` },
  })
  maps.value = res.data
}

onMounted(getMaps)

/** ✅ 임시 버튼 배치(퍼센트 좌표) */
const pinStyle = (idx) => {
  const positions = [
    { top: '18%', left: '12%' },
    { top: '30%', left: '55%' },
    { top: '48%', left: '20%' },
    { top: '60%', left: '60%' },
    { top: '75%', left: '35%' },
  ]
  const p = positions[idx % positions.length]
  return {
    top: p.top,
    left: p.left,
    transform: 'translate(-50%, -50%)',
  }
}

/** ✅ 이동 제한(맵이 뷰포트 밖으로 너무 나가지 않게 clamp)
 *  - 여기서는 “지도 레이어” 크기를 뷰포트와 같다고 가정(absolute inset-0)
 *  - scale 되면 콘텐츠가 커지므로, tx/ty 범위를 제한해야 함
 */
const clampPan = () => {
  const vp = viewportRef.value
  if (!vp) return

  const vw = vp.clientWidth
  const vh = vp.clientHeight

  // 지도 기본 크기 = 뷰포트 크기(absolute inset-0)라고 보고 계산
  const mw = vw * scale.value
  const mh = vh * scale.value

  // 좌상단 기준 transformOrigin: 0 0 이므로,
  // tx는 [-(mw - vw), 0] 범위를 유지하면 “빈 공간”이 안 생김
  const minX = Math.min(0, vw - mw)
  const minY = Math.min(0, vh - mh)

  if (tx.value < minX) tx.value = minX
  if (ty.value < minY) ty.value = minY
  if (tx.value > 0) tx.value = 0
  if (ty.value > 0) ty.value = 0
}

const onPointerDown = (e) => {
  dragging.value = true
  last.value = { x: e.clientX, y: e.clientY }
  e.currentTarget.setPointerCapture?.(e.pointerId)
}

const onPointerMove = (e) => {
  if (!dragging.value) return
  const dx = e.clientX - last.value.x
  const dy = e.clientY - last.value.y
  last.value = { x: e.clientX, y: e.clientY }

  tx.value += dx
  ty.value += dy
  clampPan()
}

const onPointerUp = () => {
  dragging.value = false
}

/** ✅ 휠로 줌: 마우스 위치를 기준으로 확대되게 만들면 UX가 좋아짐 */
const onWheel = (e) => {
  const vp = viewportRef.value
  if (!vp) return

  const rect = vp.getBoundingClientRect()
  const mx = e.clientX - rect.left
  const my = e.clientY - rect.top

  const oldScale = scale.value
  const delta = e.deltaY > 0 ? -0.1 : 0.1
  const next = Math.min(maxScale, Math.max(minScale, oldScale + delta))
  if (next === oldScale) return

  // 마우스 포인트가 화면에서 같은 위치에 보이도록 tx/ty 보정
  // (mx,my)는 뷰포트 좌표
  const sx = mx - tx.value
  const sy = my - ty.value
  const ratio = next / oldScale

  tx.value = mx - sx * ratio
  ty.value = my - sy * ratio
  scale.value = next

  clampPan()
}

const resetView = () => {
  scale.value = 1
  tx.value = 0
  ty.value = 0
}
</script>


<style scoped>
</style>