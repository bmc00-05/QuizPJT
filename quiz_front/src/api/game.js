import client from "./client"

/** 맵 목록 / 맵 상세(포함된 문제집) */
export const fetchMaps = () => client.get("/game/maps/")
export const fetchMap = (mapId) => client.get(`/game/maps/${mapId}/`)

/** 플레이 세션 시작 / 정답 채점 */
export const startPlaySession = (payload) =>
  client.post("/game/quiz/play/", payload)
export const checkAnswer = (payload) => client.post("/game/quiz/check/", payload)

/** 자유 모드 — 공개된 유저 문제집 목록 */
export const fetchUserProblemSets = () => client.get("/game/users/problemsets/")
export const fetchProblemSetsByUser = (userId) =>
  client.get(`/game/users/${userId}/problemsets/`)

/** 문제집 좋아요 토글 */
export const toggleProblemSetLike = (setId) =>
  client.post(`/game/problemsets/${setId}/like/`, {})

/** 최근 오답 기록 */
export const fetchWrongHistory = (params) =>
  client.get("/game/history/", { params })
