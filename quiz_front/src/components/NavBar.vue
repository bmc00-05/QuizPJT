<template>
  <div class="nav-panel">
    <nav class="h-16 w-full p-0 pixel-panel__content flex items-center">
      <!-- 메인(아이콘) -->
      <RouterLink :to="{ name: 'map' }" class="nav-item">
        <span class="icon-box">
          <img :src="mapIcon" alt="메인" class="icon-img" />
        </span>
      </RouterLink>

      <RouterLink :to="{ name: 'usermode' }" class="nav-item">👤유저</RouterLink>

      <RouterLink :to="{ name: 'profile' }" class="nav-item">⭐홈</RouterLink>
      <RouterLink :to="{ name: 'aimode' }" class="nav-item">🤖AI</RouterLink>
      <RouterLink :to="{ name: 'ranking' }" class="nav-item">🤖랭킹</RouterLink>
    </nav>
  </div>
</template>

<script setup>
import mapIcon from '@/assets/icons/map_icon.png'
</script>

<style scoped>
.nav-item{
  flex: 1;
  height: 100%;                 /* ✅ nav 높이(h-16)를 그대로 받음 */
  display: flex;
  align-items: center;          /* ✅ 세로 가운데 */
  justify-content: center;      /* ✅ 가로 가운데 */
}

.icon-box{
  width: 40px;                  /* ✅ 정사각형(원하면 36~48) */
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-img{
  width: 100%;
  height: 100%;
  object-fit: contain;          /* ✅ 안 잘리고 정사각형에 꽉 */
  image-rendering: pixelated;
  display: block;
}
</style>
