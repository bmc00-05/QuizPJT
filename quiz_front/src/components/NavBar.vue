<template>
  <div class="nav-panel bg-black">
    <nav class="nav-wrap pixel-panel__content p-0">
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

        <span class="content">
          <span class="icon-box">
            <img :src="item.icon" class="icon-img" :alt="item.label" />
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

const route = useRoute()
const accountStore = useAccountStore()

// ✅ 여기서 "내 id" 꺼내는 키는 너 store에 맞게 하나만 남겨도 됨
const myId = computed(() => accountStore.user?.id ?? accountStore.userId ?? null)

const items = computed(() => [
  { name: "map", label: "맵", icon: mapIcon, activeBg: bg, to: { name: "map" } },
  { name: "usermode", label: "유저", icon: userIcon, activeBg: bg, to: { name: "usermode" } },

  // ✅ profile은 id 필요!
  {
    name: "profile",
    label: "홈",
    icon: homeIcon,
    activeBg: bg,
    to: myId.value ? { name: "profile" } : { name: "map" },
    disabled: !myId.value,
  },

  { name: "aimode", label: "AI", icon: aiIcon, activeBg: bg, to: { name: "aimode" } },
  { name: "ranking", label: "랭킹", icon: rankIcon, activeBg: bg, to: { name: "ranking" } },
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
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

/* ✅ 위아래 1px 더 키우기 */
.active-bg {
  position: absolute;
  inset: -1px 0;          /* top/bottom -1px, left/right 0 */
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
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.icon-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  image-rendering: pixelated;
  display: block;
}
</style>
