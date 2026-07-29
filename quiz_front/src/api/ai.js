import client from "./client"

/** 최근 오답 기반 AI 피드백 요청 */
export const requestFeedback = ({ days = 7, limit = 20, extraInput = "" } = {}) =>
  client.post("/ai/feedback/", {
    days,
    limit,
    extra_input: extraInput,
  })

/** 지난 코칭 기록 목록 */
export const fetchFeedbackHistory = (params) =>
  client.get("/ai/feedback/history/", { params })

/** 코칭 기록 상세 */
export const fetchFeedbackDetail = (id) =>
  client.get(`/ai/feedback/history/${id}/`)

/** 코칭 기록 삭제 */
export const deleteFeedback = (id) =>
  client.delete(`/ai/feedback/history/${id}/delete/`)

/** 남은 AI 호출 횟수 (사용자당 / 전역) */
export const fetchQuota = () => client.get("/ai/quota/")
