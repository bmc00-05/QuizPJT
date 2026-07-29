import client from "./client"

/** 내가 만든 문제집 목록 / 생성 */
export const fetchMyProblemSets = () => client.get("/questions/problemsets/")
export const createProblemSet = (payload) =>
  client.post("/questions/problemsets/", payload)

/** 문제집 상세 / 수정 / 삭제 */
export const fetchProblemSet = (setId) =>
  client.get(`/questions/problemsets/${setId}/`)
export const updateProblemSet = (setId, payload) =>
  client.patch(`/questions/problemsets/${setId}/`, payload)
export const deleteProblemSet = (setId) =>
  client.delete(`/questions/problemsets/${setId}/`)

/** 문제집에 속한 문제 목록 / 문제 추가 */
export const fetchProblems = (setId) =>
  client.get(`/questions/problemsets/${setId}/problems/`)
export const createProblem = (setId, payload) =>
  client.post(`/questions/problemsets/${setId}/problems/`, payload)

/** 개별 문제 상세 / 수정 / 삭제 */
export const fetchProblem = (problemId) =>
  client.get(`/questions/problem/${problemId}/`)
export const updateProblem = (problemId, payload) =>
  client.patch(`/questions/problem/${problemId}/`, payload)
export const deleteProblem = (problemId) =>
  client.delete(`/questions/problem/${problemId}/`)
