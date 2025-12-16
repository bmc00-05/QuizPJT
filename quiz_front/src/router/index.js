import { createRouter, createWebHistory } from 'vue-router'
import StartPage from '@/views/StartPage.vue'
import LoginPage from '@/views/LoginPage.vue'
import SignUpPage from '@/views/SignUpPage.vue'
import MainPage from '@/views/MainPage.vue'
import MapPage from '@/views/MapPage.vue'
import UserModePage from '@/views/UserModePage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
  {
    path: '/',
    name: 'start',
    component: StartPage
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUpPage
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

  ],
})

export default router
