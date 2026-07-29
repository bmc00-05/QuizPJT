<template>
  <div class="relative justify-center w-full max-w-sm pixel-panel">
    <div class="pixel-panel__content">
      <button
        @click="close"
        class="absolute right-4 top-4 text-gray-400 hover:text-gray-600"
        aria-label="Close"
      >
        ✕
      </button>

      <!-- 타이틀 -->
      <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <h2 class="mt-6 text-center text-2xl font-bold tracking-tight text-gray-900">
          Create your account
        </h2>

      </div>

      <div class="mt-8">
        <form @submit.prevent="signUp" class="space-y-6">
          <div>
            <label for="username" class="block text-sm font-bold text-gray-900">
              Username
            </label>
            <div class="mt-2">
              <input
                v-model.trim="username"
                id="username"
                type="text"
                autocomplete="username"
                required
                class="block w-full input-panel-icon"
              />
            </div>
          </div>

          <div>
            <label for="email" class="block text-sm font-bold text-gray-900">
              Email
            </label>
            <div class="mt-2">
              <input
                v-model.trim="email"
                id="email"
                type="email"
                autocomplete="email"
                required
                class="block w-full input-panel-icon"
              />
            </div>
          </div>

          <div>
            <label for="password1" class="block text-sm font-bold text-gray-900">
              Password
            </label>
            <div class="mt-2">
              <input
                v-model.trim="password1"
                id="password1"
                type="password"
                autocomplete="new-password"
                required
                class="block w-full input-panel-icon"
              />
            </div>
          </div>

          <div>
            <label for="password2" class="block text-sm font-bold text-gray-900">
              Password 확인
            </label>
            <div class="mt-2">
              <input
                v-model.trim="password2"
                id="password2"
                type="password"
                autocomplete="new-password"
                required
                class="block w-full rounded-md input-panel-icon"
              />
            </div>
          </div>

        <!-- ✅ 오류 메시지 (타이틀 아래) -->
        <p
          v-if="errorMsg"
          class="mt-3 text-xs text-red-700"
          role="alert"
        >
          {{ errorMsg }}
        </p>
        
          <button
            type="submit"
            class="w-full rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
          >
            Sign Up
          </button>
        </form>

        <p class="mt-6 text-center text-sm text-gray-500">
          이미 계정이 있습니다
          <RouterLink
            :to="{ name: 'login' }"
            class="font-semibold text-indigo-600 hover:text-indigo-500"
          >
            로그인
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
const accountStore = useAccountStore()

const email = ref(null)
const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)

const errorMsg = ref('') // ✅ 화면에 표시할 에러 메시지

/**
 * ✅ 회원가입 에러를 "한글 메시지"로 통일
 * - 서버에서 오는 영문 문구/키 값을 그대로 노출하지 않게 함
 * - DRF/dj-rest-auth/allauth 계열 에러 형태 대응
 */
const toKoreanSignupError = (status, data) => {
  // 네트워크/응답 없음
  if (!data && !status) return '서버에 연결할 수 없습니다. 네트워크 상태를 확인해주세요.'
  if (!data) return '회원가입에 실패했습니다. 잠시 후 다시 시도해주세요.'

  // 문자열로 오는 경우(detail 등)
  if (typeof data === 'string') return '회원가입에 실패했습니다. 입력값을 확인해주세요.'

  // ✅ 공통 키들
  const detail = data?.detail
  const nonField = data?.non_field_errors?.[0]

  // ✅ 필드별 에러(배열 형태가 많음)
  const emailErr = data?.email?.[0]
  const userErr = data?.username?.[0]
  const p1Err = data?.password1?.[0]
  const p2Err = data?.password2?.[0]

  // ✅ 1) non_field/detail 은 보통 "중복/자격/일반 실패" → 한글로 통일
  if (nonField || detail) {
    // 비밀번호 불일치가 non_field로 올 때도 있어 체크
    const msg = (nonField || detail || '').toString().toLowerCase()
    if (msg.includes('password') && msg.includes('match')) {
      return '비밀번호가 일치하지 않습니다.'
    }
    return '회원가입에 실패했습니다. 입력값을 확인해주세요.'
  }

  // ✅ 2) email
  if (emailErr) {
    const msg = String(emailErr).toLowerCase()
    if (msg.includes('valid') || msg.includes('invalid')) return '이메일 형식이 올바르지 않습니다.'
    if (msg.includes('already') || msg.includes('exists')) return '이미 사용 중인 이메일입니다.'
    return '이메일을 확인해주세요.'
  }

  // ✅ 3) username
  if (userErr) {
    const msg = String(userErr).toLowerCase()
    if (msg.includes('already') || msg.includes('exists') || msg.includes('taken')) return '이미 사용 중인 아이디입니다.'
    if (msg.includes('required')) return '아이디를 입력해주세요.'
    return '아이디를 확인해주세요.'
  }

  // ✅ 4) password1 / password2
  if (p1Err || p2Err) {
    const msg = String(p1Err || p2Err).toLowerCase()
    if (msg.includes('match')) return '비밀번호가 일치하지 않습니다.'
    if (msg.includes('too short') || msg.includes('minimum')) return '비밀번호가 너무 짧습니다.'
    if (msg.includes('common')) return '비밀번호가 너무 쉬워요. 더 복잡하게 설정해주세요.'
    if (msg.includes('numeric')) return '비밀번호를 숫자만으로 설정할 수 없습니다.'
    return '비밀번호를 확인해주세요.'
  }

  // ✅ 5) 혹시 다른 키로 올 때: 첫 에러 키만 보고 일반 안내
  const firstKey = Object.keys(data)[0]
  if (firstKey) return '회원가입 정보가 올바르지 않습니다. 입력값을 확인해주세요.'

  return '회원가입에 실패했습니다. 입력값을 확인해주세요.'
}

const signUp = async () => {
  errorMsg.value = ''

  // (선택) 프론트에서 먼저 잡기: 비번 불일치
  if (password1.value !== password2.value) {
    errorMsg.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  const payload = {
    email: email.value,
    username: username.value,
    password1: password1.value,
    password2: password2.value,
  }

  try {
    await accountStore.signUp(payload)

    // ✅ 회원가입 성공 후 자동 로그인
    await accountStore.logIn({
      username: payload.username,
      password: payload.password1,
    })

    router.push({ name: 'start' })
  } catch (err) {
    const status = err?.response?.status
    const data = err?.response?.data

    errorMsg.value = toKoreanSignupError(status, data)

    // 디버그는 콘솔로만
    console.log('signup error status:', status)
    console.log('signup error data:', data)
  }
}

const close = () => {
  router.push({ name: 'start' })
}

// ✅ 입력 수정하면 에러 메시지 자동 제거
watch([email, username, password1, password2], () => {
  errorMsg.value = ''
})

</script>

<style scoped></style>
