import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAccountStore = defineStore('account', () => {

  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)

  const router = useRouter()

  const signUp = async (payload) => {
    try {
      const res = await axios.post(
        `${API_URL}/accounts/signup/`,
        payload
      )
      return res

    } catch (err) {
      throw err
    }
  }

  const logIn = async (payload) => {

    try {
    const res = await axios.post(
      `${API_URL}/accounts/login/`,
      payload
    )
    console.log(res)
    token.value = res.data.key   // 상태만 변경
    return res

    } catch (err) {
      throw err
    }
  }

  const isLogin = computed(() => {
    return token.value ? true : false
  })

  const logOut = () => {
    token.value = null
    router.push({ name: 'start' })
  }

  return { token, signUp, logIn, logOut, isLogin }
}, { persist: true }) 
