import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

import router from '@/router'
import * as accountsApi from '@/api/accounts'

export const useAccountStore = defineStore('account', () => {

  const token = ref(null)
  const user = ref(null)

  const signUp = async (payload) => {
    const res = await accountsApi.signUp(payload)
    return res.data
  }

  const fetchMe = async () => {
    if (!token.value) return null
    const res = await accountsApi.fetchMe()
    user.value = res.data
    return res.data
  }

  const logIn = async (payload) => {
    const res = await accountsApi.logIn(payload)

    token.value = res.data.key
    await fetchMe()

    return res
  }

  const isLogin = computed(() => {
    return token.value ? true : false
  })

  const userId = computed(() => user.value?.pk ?? null)

  const logOut = () => {
    token.value = null
    user.value = null
    // useRouter() 대신 라우터 인스턴스를 직접 import 한다.
    // useRouter() 는 컴포넌트 setup 컨텍스트에서만 보장되므로,
    // 스토어가 컴포넌트 밖에서 처음 사용되면 undefined 가 될 수 있다.
    router.push({ name: 'start' })
  }

  return { token, user, userId, signUp, logIn, logOut, fetchMe, isLogin }
}, { persist: true })
