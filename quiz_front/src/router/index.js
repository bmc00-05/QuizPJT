import { createRouter, createWebHistory /* or createWebHashHistory */ } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { useUserStore } from '@/stores/user'

import StartPage from '@/views/StartPage.vue'
import LoginPage from '@/components/LoginPage.vue'
import SignUpPage from '@/components/SignUpPage.vue'
import MainPage from '@/views/MainPage.vue'

import Map from '@/views/Map.vue'
import GameView from '@/views/GameView.vue'
import UserMode from '@/views/UserMode.vue'
import Profile from '@/views/Profile.vue'
import MyProblemSet from '@/views/MyProblemSet.vue'
import AIMode from '@/views/AIMode.vue'
import Ranking from '@/views/Ranking.vue'

const router = createRouter({
  // ✅ 루트+서버 fallback 가능하면 이거 유지
  history: createWebHistory(import.meta.env.BASE_URL),

  // ✅ base './' + 정적호스팅이면 이게 더 안전
  // history: createWebHashHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      component: StartPage,
      children: [
        { path: '', name: 'start', component: StartPage }, // (선택) start 라우트 명확히
        { path: 'login', name: 'login', component: LoginPage },
        { path: 'signup', name: 'signup', component: SignUpPage },
      ],
    },

    {
      path: '/main',
      component: MainPage,
      meta: { requiresAuth: true },

      // ✅ /main 진입 시 기본 화면
      redirect: { name: 'map' },

      children: [
        { path: 'map', name: 'map', component: Map, meta: { requiresAuth: true } },
        { path: 'game/:id', name: 'game', component: GameView, meta: { requiresAuth: true } },
        { path: 'usermode', name: 'usermode', component: UserMode, meta: { requiresAuth: true } },
        { path: 'profile', name: 'profile', component: Profile, meta: { requiresAuth: true } },
        { path: 'profile/problemset', name: 'myproblemset', component: MyProblemSet, meta: { requiresAuth: true } },
        { path: 'ai', name: 'aimode', component: AIMode, meta: { requiresAuth: true } },
        { path: 'ranking', name: 'ranking', component: Ranking, meta: { requiresAuth: true } },
      ],
    },
  ],
})

router.beforeEach(async (to) => {
  const accountStore = useAccountStore()
  const userStore = useUserStore()

  // ✅ /main 하위 전부 보호
  if (to.meta.requiresAuth && !accountStore.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'login' }
  }

  // ✅ 로그인 상태면 로그인/회원가입 막기
  if ((to.name === 'signup' || to.name === 'login') && accountStore.isLogin) {
    window.alert('이미 로그인 되어 있습니다.')
    return { name: 'map' } // start 말고 실제 메인으로 보내는게 UX 보통 더 좋음
  }

  // ✅ 로그인 상태인데 유저정보 미로딩이면 1회 로드
  if (accountStore.isLogin && !userStore.loaded) {
    try {
      await userStore.fetchUser()
    } catch (err) {
      accountStore.logOut?.()
      return { name: 'login' }
    }
  }

  return true
})

export default router
