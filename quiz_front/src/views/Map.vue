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
  class="absolute z-10"
  :style="pinStyle(idx)"
  @click.stop="selectMap(map)"
  @pointerdown.stop
  @mouseenter="hoverId = map.id"
  @mouseleave="hoverId = null"
>
  <div class="flex flex-col items-center gap-0">
    <img
      :src="getMapIcon(map)"
      alt=""
      class="w-[56px] h-[56px] [image-rendering:pixelated]
             drop-shadow-md transition-transform
             hover:scale-110 active:scale-95"
      draggable="false"
    />
    <span class="text-[11px] font-bold text-white drop-shadow">
      {{ map.name }}
    </span>
  </div>
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
      <div class="ml-2 mb-1 text-lg font-bold">
          {{ currentMapName }}
        <!-- 난이도 -->
        <span v-if="problemSetData" class="mt-2 text-sm text-gray-800">
            {{ problemSetData.title }}  
        </span>                     
          <!-- 지역명 -->
          <div class="font-bold text-sm min-h-[20px]">
              {{ currentRegionName }}
          </div>

        </div>



<!-- 썸네일/배너 -->
<div class="w-full h-28 input-panel-icon rounded mb-2 overflow-hidden bg-black/10">
<img
  :src="currentBannerUrl"
  alt=""
  class="w-full h-full object-cover [image-rendering:pixelated]"
  draggable="false"
/>
</div>

    <p class="input-panel-icon text-xs font-normal">{{ currentDescriptionText }}</p>
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
  class="button-panel w-full max-w-[100px]"
  @click="openModal()"
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
  </div>
</div>

    

<BaseModal v-if="modal.isOpen && problemSetData" @close="closeModal">
  <div class="text-black w-[92vw] max-w-[300px]">
    <div class="">
      <div class=" flex flex-col gap-3">

        <!-- 헤더 -->
        <div class="text-center">
          <div class="text-[13px] font-black tracking-widest">
            {{ currentMapName }}
          </div>
          <div class="text-[11px] opacity-80 mt-0.5">
            {{ currentRegionName }}
          </div>

          <div class="mt-2 inline-flex items-center gap-2">
            <span class="text-[11px] opacity-70">난이도</span>
            <span class="text-[12px] font-bold">
              {{ problemSetData.title }}
            </span>
          </div>
        </div>

        <!-- 선택된 맵 이미지 -->
        <div class="w-full h-28 input-panel-icon overflow-hidden bg-black/10">
          <img
            :src="currentBannerUrl"
            alt=""
            class="w-full h-full object-cover [image-rendering:pixelated]"
            draggable="false"
          />
        </div>

        <!-- 설명 -->
        <div class="input-panel-icon px-2 py-2 text-[11px] leading-relaxed">
          <div class="font-bold mb-1">진입 안내</div>
          <div class="opacity-90">
            {{ currentRegionName}}
          </div>
          <div class="mt-2 font-bold">
            퀴즈 세션에 진입하겠습니까?
          </div>
        </div>

        <!-- 버튼 -->
        <div class="grid grid-cols-2 gap-2">
          <button type="button" class="button-panel" @click="closeModal">
            <div class="pixel-panel__content p-2 text-center font-bold">취소</div>
          </button>

          <RouterLink
            class="button-panel"
            :to="{ name: 'game', params: { id: problemSetData.id } }"
            @click="closeModal"
          >
            <div class="pixel-panel__content p-2 text-center font-bold">퀴즈 시작</div>
          </RouterLink>
        </div>

      </div>
    </div>
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
import iconDefault from "@/assets/mapicons/default.png"

import lake_normal from "@/assets/mapicons/lake_normal.png"
import lake_hover from "@/assets/mapicons/lake_hover.png"
import forest_normal from "@/assets/mapicons/forest_normal.png"
import forest_hover from "@/assets/mapicons/forest_hover.png"
import cave_normal from "@/assets/mapicons/cave_normal.png"
import cave_hover from "@/assets/mapicons/cave_hover.png"
import castle_normal from "@/assets/mapicons/castle_normal.png"
import castle_hover from "@/assets/mapicons/castle_hover.png"
import mountain_normal from "@/assets/mapicons/mountain_normal.png"
import mountain_hover from "@/assets/mapicons/mountain_hover.png"

import bannerDefault from "@/assets/background/camp.png"

import bannerMap1 from "@/assets/banners/lake_main.jpg"
import bannerMap2 from "@/assets/banners/forest_main.jpg"
import bannerMap3 from "@/assets/banners/cave_main.jpg"
import bannerMap4 from "@/assets/banners/castle_main.jpg"
import bannerMap5 from "@/assets/banners/mountain_main.jpg"

import lake_easy_banner from "@/assets/banners/lake_easy.jpg"
import lake_normal_banner from "@/assets/banners/lake_normal.jpg"
import lake_hard_banner from "@/assets/banners/lake_hard.jpg"

import forest_easy_banner from "@/assets/banners/forest_easy.jpg"
import forest_normal_banner from "@/assets/banners/forest_normal.jpg"
import forest_hard_banner from "@/assets/banners/forest_hard.jpg"

import cave_easy_banner from "@/assets/banners/cave_easy.jpg"
import cave_normal_banner from "@/assets/banners/cave_normal.jpg"
import cave_hard_banner from "@/assets/banners/cave_hard.jpg"

import castle_easy_banner from "@/assets/banners/castle_easy.jpg"
import castle_normal_banner from "@/assets/banners/castle_normal.jpg"
import castle_hard_banner from "@/assets/banners/castle_hard.jpg"

import mountain_easy_banner from "@/assets/banners/mountain_easy.jpg"
import mountain_normal_banner from "@/assets/banners/mountain_normal.jpg"
import mountain_hard_banner from "@/assets/banners/mountain_hard.jpg"

const MAP_BANNER_BY_ID = {
  1: bannerMap1,
  2: bannerMap2,
  3: bannerMap3,
  4: bannerMap4,
  5: bannerMap5,
}

const MAP_DIFFICULTY_BANNER = {
  1: { easy: lake_easy_banner, normal: lake_normal_banner, hard: lake_hard_banner },
  2: { easy: forest_easy_banner, normal: forest_normal_banner, hard: forest_hard_banner },
  3: { easy: cave_easy_banner, normal: cave_normal_banner, hard: cave_hard_banner },
  4: { easy: castle_easy_banner, normal: castle_normal_banner, hard: castle_hard_banner },
  5: { easy: mountain_easy_banner, normal: mountain_normal_banner, hard: mountain_hard_banner },

}

const currentBannerUrl = computed(() => {
  const mapId = mapData.value?.id
  if (!mapId) return bannerDefault

  const diff = selectedDifficulty.value
  if (diff && MAP_DIFFICULTY_BANNER[mapId]?.[diff]) {
    return MAP_DIFFICULTY_BANNER[mapId][diff]
  }

  // 난이도 아직 선택 안 했으면 맵 기본 배너
  return MAP_BANNER_BY_ID[mapId] ?? bannerDefault
})

// const getMapBanner = (map) => {
//   if (!map) return bannerDefault
//   return MAP_BANNER[map.id] ?? bannerDefault
// }

const API_URL = import.meta.env.VITE_REST_API_URL
const modal = useModalStore()
const accountStore = useAccountStore()
const maps = ref([])

const hoverId = ref(null)

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

// ✅ map.id 기준 매핑 (네 maps 데이터의 id에 맞게)
const MAP_ICON = {
  1: { normal: lake_normal, selected: lake_hover },
  2: { normal: forest_normal, selected: forest_hover },
  3: { normal: cave_normal, selected: cave_hover },
  4: { normal: castle_normal, selected: castle_hover },
  5: { normal: mountain_normal, selected: mountain_hover },
  // ...
}

// ✅ 맵 기본 설명(난이도 선택 전)
const MAP_STORY = {
  1: "잔잔한 호숫가. 초보 모험가들이 첫 발을 떼는 곳이다.",
  2: "짙은 숲. 길을 잃기 쉽고, 소리 없는 위험이 숨어 있다.",
  3: "동굴. 어둠 속에서 작은 실수 하나가 큰 대가가 된다.",
  4: "성. 규칙과 함정이 얽힌 거대한 미궁.",
  5: "산. 높은 곳일수록 바람은 차갑고, 시험은 더 험하다.",
}

// ✅ 난이도(=지역) 선택 후 설명(맵 + 난이도 조합)
const REGION_STORY = {
  1: {
    easy: "호숫가 산책로. 기본기를 다지기 좋은 구간.",
    normal: "수로 유적. 선택과 집중이 중요해진다.",
    hard: "호수 깊은 곳. 신비로운 기운이 느껴진다.",
  },
  2: {
    easy: "숲 입구. 길은 단순하지만 방심 금지.",
    normal: "그늘 숲길. 주변에서 맹수의 시선이 느껴진다.",
    hard: "깊은 숲 중앙 신비로운 기운이 느껴진다.",
  },
  3: {
    easy: "동굴 초입. 수많은 수정들이 동굴 안을 장식한다.",
    normal: "흔들 다리 구간. 항상 조심할 것.",
    hard: "심층 용암 지대. 뜨거워서 온몸이 타버릴 것 같다.",
  },
  4: {
    easy: "도서관. 구조 파악부터 시작.",
    normal: "지하 감옥. 어둡고 축축하다.",
    hard: "왕좌의 방. 가장 높은 수준의 시험.",
  },
  5: {
    easy: "산기슭. 리듬을 만들기 좋은 코스.",
    normal: "폐광. 오랫동안 방치된 것 같다.",
    hard: "정상 설원. 끝까지 흔들리지 마라.",
  },
}
const currentMapName = computed(() => mapData.value?.name ?? "")

const currentDescriptionText = computed(() => {
  const mapId = mapData.value?.id
  if (!mapId) return ""

  const diff = selectedDifficulty.value

  // ✅ 난이도 선택된 경우: 맵+난이도 설명 우선
  if (diff) {
    return (
      REGION_STORY[mapId]?.[diff] ??
      problemSetData.value?.description ??   // 서버/DB 설명 fallback
      MAP_STORY[mapId] ??
      mapData.value?.description ??
      ""
    )
  }

  // ✅ 난이도 선택 전: 맵 기본 설명
  return MAP_STORY[mapId] ?? mapData.value?.description ?? ""
})


const getMapIcon = (map) => {
  const pack = MAP_ICON[map.id]
  if (!pack) return iconDefault

  const isHovered = hoverId.value === map.id
  const isSelected = mapData.value?.id === map.id

  return (isHovered || isSelected) ? pack.selected : pack.normal
}


// ✅ 난이도 키: activeBtn -> 'easy' | 'normal' | 'hard'
const selectedDifficulty = computed(() => {
  if (activeBtn.value === "easy") return "easy"
  if (activeBtn.value === "normal") return "normal"
  if (activeBtn.value === "hard") return "hard"
  return null
})

/** ✅ 맵 + 난이도별 지역명 사전 */
const REGION_NAME = {
  1: { easy: "호숫가 산책로", normal: "수로 유적", hard: "호수 깊은 곳" },
  2: { easy: "숲 입구",     normal: "그늘 숲길",   hard: "신비한 나무" },
  3: { easy: "동굴 초입",   normal: "흔들 다리 구간",   hard: "심층 용암 지대" },
  4: { easy: "도서관",     normal: "지하 감옥",   hard: "왕좌의 방" },
  5: { easy: "산기슭",     normal: "폐광",     hard: "정상 설원" },
}

/** ✅ 지역명: 사전 우선 -> 없으면 problemSetData.description fallback */
const currentRegionName = computed(() => {
  const mapId = mapData.value?.id
  const diff = selectedDifficulty.value
  if (!mapId) return ""

  // ✅ 난이도 선택된 경우: 사전 지역명 우선
  if (diff && REGION_NAME[mapId]?.[diff]) {
    return REGION_NAME[mapId][diff]
  }

  // ✅ 난이도 미선택 or 사전 없을 때: 기존 데이터 fallback
  return problemSetData.value?.description ?? ""
})
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
    { top: '25%', left: '38%' },
    { top: '57%', left: '35%' },
    { top: '40%', left: '52%' },
    { top: '85%', left: '77%' },
    { top: '88%', left: '53%' },
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