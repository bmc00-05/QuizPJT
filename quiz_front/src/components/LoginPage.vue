<template>



    <!-- 카드 -->
    <div class="relative justify-center w-full max-w-sm pixel-panel">
      <div class="pixel-panel__content">
      <!-- 닫기 버튼 -->
      <button
        @click="close"
        class="absolute right-4 top-4 text-gray-400 hover:text-gray-600"
        aria-label="Close"
      >
        ✕
      </button>

      <!-- 로고 & 타이틀 -->
      <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <h2 class="mt-6 text-center text-2xl font-bold tracking-tight text-gray-900">
          Sign in to your account
        </h2>
      </div>

      <!-- 로그인 폼 -->
      <div class="mt-8">
                  <!-- ✅ 에러 메시지 -->
 
        <form @submit.prevent="login" class="space-y-6">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-900">
              ID
            </label>
            <div class="mt-2">
              <input
                v-model.trim="username"
                id="username"
                type="text"
                autocomplete="username"
                required
                class="block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-900">
              Password
            </label>
            <div class="mt-2">
              <input
                v-model.trim="password"
                id="password"
                type="password"
                autocomplete="current-password"
                required
                class="block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>
          </div>
          <div
            v-if="errorMsg"
            class="mb-4 text-xs text-red-700"
          >
            {{ errorMsg }}
          </div>

          <button
            type="submit"
            class="w-full rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
          >
            Sign in
          </button>
        </form>

        <p class="mt-6 text-center text-sm text-gray-500">
          회원이 아니신가요?
          <RouterLink
            :to="{ name: 'signup' }"
            class="font-semibold text-indigo-600 hover:text-indigo-500"
          >
            회원가입
          </RouterLink>
        </p>
      </div>
    </div>
    </div>

</template>

<script setup>
import { ref, watch } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref(null)
const password = ref(null)

const accountStore = useAccountStore()

// ✅ 화면에 표시할 에러 메시지
const errorMsg = ref('')

const login = async () => {
  errorMsg.value = ''

  const payload = {
    username: username.value,
    password: password.value,
  }

  try {
    await accountStore.logIn(payload)
    router.push({ name: 'start' })
  } catch (err) {
    const status = err?.response?.status
    const data = err?.response?.data

    if (status === 400) {
      const nonField = data?.non_field_errors?.[0]
      const userErr = data?.username?.[0]
      const passErr = data?.password?.[0]
      const detail = data?.detail

      // ✅ 핵심: 서버 영문(non_field_errors / detail)은 화면에 그대로 뿌리지 말고 한글로 통일
      if (nonField || detail) {
        errorMsg.value = '아이디 또는 비밀번호가 올바르지 않습니다.'
      } else if (userErr) {
        errorMsg.value = '아이디를 확인해주세요.'
      } else if (passErr) {
        errorMsg.value = '비밀번호를 확인해주세요.'
      } else {
        errorMsg.value = '입력값이 올바르지 않습니다.'
      }

    } else if (status === 401) {
      errorMsg.value = '아이디 또는 비밀번호가 올바르지 않습니다.'
    } else if (!err?.response) {
      errorMsg.value = '서버에 연결할 수 없습니다. 네트워크 상태를 확인해주세요.'
    } else {
      errorMsg.value = '로그인 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
    }
  }
}

const close = () => {
  router.push({ name: 'start' })
}

watch([username, password], () => {
  errorMsg.value = ''
})
</script>


<style scoped>

</style>

