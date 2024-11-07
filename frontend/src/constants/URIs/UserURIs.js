import { HOST, ID, KEY } from "./General"

export const BASE = `${HOST}/api/user/v1`

export const REGISTER               = `${BASE}/register`
export const LOGIN                  = `${BASE}/login`
export const LOGOUT                 = `${BASE}/logout`
export const USER_DATA              = `${BASE}/user/data`
export const EMAIL_VERIFICATION     = `/${ID}/${KEY}`
