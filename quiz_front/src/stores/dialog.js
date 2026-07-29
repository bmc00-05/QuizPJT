import { defineStore } from "pinia"
import { ref } from "vue"

/**
 * 브라우저 기본 alert / confirm 을 대체하는 전역 다이얼로그.
 *
 * 픽셀 아트 톤의 화면에서 OS 기본 팝업이 뜨면 몰입이 끊기고
 * 완성도가 크게 떨어져 보인다. BaseModal 을 재사용해 앱 안에서 처리한다.
 *
 * 사용:
 *   const dialog = useDialogStore()
 *   dialog.alert("문제집을 삭제했습니다.")
 *   if (await dialog.confirm("정말 삭제할까요?")) { ... }
 */
export const useDialogStore = defineStore("dialog", () => {
  const isOpen = ref(false)
  const title = ref("")
  const message = ref("")
  const mode = ref("alert") // "alert" | "confirm"
  const tone = ref("info") // "info" | "danger"
  const confirmText = ref("확인")

  // confirm 의 결과를 await 로 받기 위한 resolver
  let resolver = null

  const close = (result) => {
    isOpen.value = false
    if (resolver) {
      resolver(result)
      resolver = null
    }
  }

  const open = (options) => {
    title.value = options.title ?? ""
    message.value = options.message ?? ""
    mode.value = options.mode ?? "alert"
    tone.value = options.tone ?? "info"
    confirmText.value = options.confirmText ?? "확인"
    isOpen.value = true

    return new Promise((resolve) => {
      resolver = resolve
    })
  }

  /** 알림. 확인을 누르면 resolve 된다. */
  const alert = (message, options = {}) =>
    open({ ...options, message, mode: "alert" })

  /** 확인. 확인이면 true, 취소·닫기면 false 로 resolve 된다. */
  const confirm = (message, options = {}) =>
    open({ ...options, message, mode: "confirm" })

  return {
    isOpen,
    title,
    message,
    mode,
    tone,
    confirmText,
    alert,
    confirm,
    close,
  }
})
