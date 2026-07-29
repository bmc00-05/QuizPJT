import client from "./client"

/** 내 프로필 기본 정보 */
export const fetchProfile = () => client.get("/profile/")

/** 내 상태(스탯). userId 를 주면 다른 사용자 조회 */
export const fetchStatus = (userId) =>
  client.get(userId ? `/profile/status/${userId}/` : "/profile/status/")

/** 랭킹 */
export const fetchRanking = () => client.get("/profile/ranking/")

/** 뱃지 도감 */
export const fetchBadges = () => client.get("/profile/badges/")

export const equipBadge = (badgeId) =>
  client.post("/profile/equip-badge/", { badge_id: badgeId })

export const unequipBadge = () => client.post("/profile/unequip-badge/", {})

/** 신규 획득 뱃지 확인 처리 */
export const ackNewBadges = (codes) =>
  client.post("/profile/me/badges/ack/", { codes })

/** 메모장 */
export const fetchMemo = () => client.get("/profile/memo/")
export const saveMemo = (memo) => client.patch("/profile/memo/", { memo })
