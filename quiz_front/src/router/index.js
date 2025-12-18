import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import StartPage from '@/views/StartPage.vue'
import LoginPage from '@/components/LoginPage.vue'
import SignUpPage from '@/components/SignUpPage.vue'
import MainPage from '@/views/MainPage.vue'
import MapPage from '@/views/MapPage.vue'
import UserModePage from '@/views/UserModePage.vue'
import MapProblemSetPage from '@/views/MapProblemSetPage.vue'
import UserPage from '@/views/UserPage.vue'
import AIPage from '@/views/AIPage.vue'
import GameView from '@/views/GameView.vue'
import CreateQuizSet from '@/components/CreateQuizSet.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
  {
    path: '/',
    name: 'start',
    component: StartPage,
    children: [
        { path: '/login', name: 'login', component: LoginPage },
        { path: '/signup', name: 'signup', component: SignUpPage },
    ]

  },
  {
    path: '/main',
    name: 'main',
    component: MainPage
  },
  {
    path: '/map',
    name: 'map',
    component: MapPage
  },
  {
    path: '/quiz/user',
    name: 'usermode',
    component: UserModePage
  },
  {
    path: '/map/:problemset',
    name: 'mainproblemset',
    component: MapProblemSetPage
  },
  {
    path: '/profile/:id',
    name: 'profile',
    component: UserPage
  },
  {
    path: '/ai',
    name: 'ai',
    component: AIPage
  },
  {
    path: '/game/:problemSetId',
    name: 'game',
    component: GameView
  },
  {
    path: '/quiz/create-set/',
    name: 'createQuizSet',
    component: CreateQuizSet
  },

  ],
})


router.beforeEach((to, from) => {
  const accountStore = useAccountStore()

  if (to.name === 'main' && !accountStore.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'LogInView' }
  }

  if ((to.name === 'signup' || to.name === 'login') && (accountStore.isLogin) ) {
    window.alert('이미 로그인 되어 있습니다.')
    return { name: 'ArticleView' }
  }
})

export default router
