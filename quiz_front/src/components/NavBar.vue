<template>
  <div class="nav-panel bg-black">
    <nav class="nav-wrap pixel-panel__content p-0 overflow-visible">
      <RouterLink
        v-for="item in items"
        :key="item.name"
        :to="item.to"
        class="nav-item"
        :class="[
          { active: isActive(item) },
          item.disabled ? 'opacity-40 pointer-events-none' : '',
        ]"
      >
        <!-- active 배경 -->
        <img
          v-if="isActive(item)"
          :src="item.activeBg"
          class="active-bg"
          alt=""
          draggable="false"
        />

        <!-- 호버 툴팁: 아이콘만으로는 무슨 탭인지 알기 어렵다 -->
        <span class="nav-tip">{{ item.label }}</span>

        <span class="content">
          <span class="icon-box">
            <!--
              두 이미지를 겹쳐 두고 CSS 로 전환한다.
              :src 를 바꾸는 방식은 첫 호버 시점에 이미지를 처음 내려받아 깜빡인다.
            -->
            <img :src="item.icon" class="icon-img icon-base" :alt="item.label" />
            <img
              :src="item.iconHover"
              class="icon-img icon-hover"
              alt=""
              aria-hidden="true"
              draggable="false"
            />
          </span>
        </span>
      </RouterLink>
    </nav>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import { useAccountStore } from "@/stores/accounts"

import bg from "@/assets/ui/nav_click.png"
import mapIcon from "@/assets/icons/map_icon.png"
import userIcon from "@/assets/icons/user_icon.png"
import homeIcon from "@/assets/icons/home_icon.png"
import aiIcon from "@/assets/icons/ai_icon.png"
import rankIcon from "@/assets/icons/rank_icon.png"

import mapIconHover from "@/assets/icons/map_icon_hover.png"
import userIconHover from "@/assets/icons/user_icon_hover.png"
import homeIconHover from "@/assets/icons/home_icon_hover.png"
import aiIconHover from "@/assets/icons/ai_icon_hover.png"
import rankIconHover from "@/assets/icons/rank_icon_hover.png"

const route = useRoute()
const accountStore = useAccountStore()

// ✅ 여기서 "내 id" 꺼내는 키는 너 store에 맞게 하나만 남겨도 됨
const myId = computed(() => accountStore.user?.id ?? accountStore.userId ?? null)

const items = computed(() => [
  {
    name: "map",
    label: "맵",
    icon: mapIcon,
    iconHover: mapIconHover,
    activeBg: bg,
    to: { name: "map" },
  },
  {
    name: "usermode",
    label: "유저",
    icon: userIcon,
    iconHover: userIconHover,
    activeBg: bg,
    to: { name: "usermode" },
  },

  // ✅ profile은 id 필요!
  {
    name: "profile",
    label: "홈",
    icon: homeIcon,
    iconHover: homeIconHover,
    activeBg: bg,
    to: myId.value ? { name: "profile" } : { name: "map" },
    disabled: !myId.value,
  },

  {
    name: "aimode",
    label: "AI",
    icon: aiIcon,
    iconHover: aiIconHover,
    activeBg: bg,
    to: { name: "aimode" },
  },
  {
    name: "ranking",
    label: "랭킹",
    icon: rankIcon,
    iconHover: rankIconHover,
    activeBg: bg,
    to: { name: "ranking" },
  },
])

const isActive = (item) => route.name === item.name
</script>

<style scoped>
.nav-wrap {
  height: 64px;
  width: 100%;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
}

.nav-item {
  position: relative;
  /* 툴팁이 위로 튀어나와야 하므로 클리핑하지 않는다.
     .active-bg 는 inset 으로 범위가 정해져 있어 넘칠 일이 없다. */
  overflow: visible;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

/* ✅ 위아래 1px 더 키우기 */
.active-bg {
  position: absolute;
  inset: 1px 0;          /* top/bottom -1px, left/right 0 */
  object-fit: cover;
  image-rendering: pixelated;
  z-index: 0;
}

.content {
  position: relative;
  z-index: 1;
  font-weight: 700;
  color: white;
}

.icon-box {
  /* span 은 기본이 inline 이라 width/height 가 적용되지 않는다.
     자식 이미지를 absolute 로 깔기 위한 기준 박스이므로 block 이어야 한다. */
  display: block;
  position: relative;
  width: 40px;
  height: 40px;
}

.icon-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  image-rendering: pixelated;
  display: block;
}

.icon-hover {
  opacity: 0;
}

/*
  아이콘 위에 떠오르는 라벨.
  마우스가 있는 환경에서만 보이므로 9-slice 패널 대신 가벼운 형태로 둔다.
  폰트는 전역 픽셀 폰트(Galmuri11)를 그대로 물려받아 톤을 맞춘다.
*/
.nav-tip {
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%) translateY(4px);
  z-index: 30;

  padding: 2px 8px;
  background: rgba(23, 23, 23, 0.92);
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  line-height: 1.4;
  letter-spacing: 0.02em;
  white-space: nowrap;

  opacity: 0;
  pointer-events: none;
  transition: opacity 120ms ease-out, transform 120ms ease-out;
}

/* 말풍선 꼬리 */
.nav-tip::after {
  content: "";
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 4px solid transparent;
  border-top-color: rgba(23, 23, 23, 0.92);
}

@media (hover: hover) {
  .nav-item:hover .nav-tip {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/*
  hover: hover 로 감싼다.
  터치 기기에서는 탭 후 hover 상태가 남아 아이콘이 바뀐 채로 고정될 수 있다.
*/
@media (hover: hover) {
  .nav-item:hover .icon-base {
    opacity: 0;
  }
  .nav-item:hover .icon-hover {
    opacity: 1;
  }
}

/* 현재 위치한 탭은 호버 아이콘을 유지해 선택 상태를 강조한다 */
.nav-item.active .icon-base {
  opacity: 0;
}
.nav-item.active .icon-hover {
  opacity: 1;
}
</style>
