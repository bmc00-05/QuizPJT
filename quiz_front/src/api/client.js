import axios from "axios"
import router from "@/router"
import { useAccountStore } from "@/stores/accounts"

/**
 * 백엔드 API 전용 axios 인스턴스.
 *
 * 이전에는 21개 파일이 각자 axios 를 import 하고 baseURL 을 조합했으며,
 * Authorization 헤더를 30곳에서 손으로 붙이고 있었다.
 * 하나만 빠뜨려도 401 이 나는 구조였고, 401 전역 처리도 없어
 * 토큰이 만료되면 화면이 조용히 비어버렸다.
 */
const client = axios.create({
  baseURL: import.meta.env.VITE_REST_API_URL,
})

/**
 * 요청마다 토큰을 자동 부착한다.
 *
 * useAccountStore() 를 모듈 최상단이 아니라 인터셉터 안에서 호출하는 것이 중요하다.
 * client.js -> stores/accounts -> client.js 순환 참조를 피하고,
 * Pinia 가 초기화된 뒤에 스토어에 접근하기 위함이다.
 */
client.interceptors.request.use((config) => {
  const account = useAccountStore()
  if (account.token) {
    config.headers.Authorization = `Token ${account.token}`
  }
  return config
})

/**
 * 401 이면 만료된 토큰을 정리하고 로그인 화면으로 보낸다.
 *
 * 토큰은 pinia-plugin-persistedstate 로 localStorage 에 남으므로,
 * 만료된 값이 새로고침 후에도 복원된다. 여기서 끊어주지 않으면
 * 사용자는 로그인 상태로 보이지만 모든 요청이 실패하는 상태에 갇힌다.
 */
client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const account = useAccountStore()

      // account.logOut() 을 쓰지 않는다.
      // logOut() 은 내부에서 start 로 이동하고, 그때 쓰는 router 는
      // 스토어 안에서 useRouter() 로 잡은 값이라 컴포넌트 컨텍스트 밖에서는
      // 보장되지 않는다. 여기서는 상태만 정리하고 이동은 직접 처리한다.
      account.token = null

      if (router.currentRoute.value.name !== "login") {
        router.push({ name: "login" })
      }
    }
    return Promise.reject(error)
  }
)

export default client
