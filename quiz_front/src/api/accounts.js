import client from "./client"

export const signUp = (payload) => client.post("/accounts/signup/", payload)
export const logIn = (payload) => client.post("/accounts/login/", payload)

/** 현재 로그인한 사용자 정보 */
export const fetchMe = () => client.get("/accounts/user/")
