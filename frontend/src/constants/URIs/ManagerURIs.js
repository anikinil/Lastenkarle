import { HOST, ID } from "./General";

export const STORE_NAME = `{STORE_NAME}`

const BASE                              = `${HOST}/api/manager/v1/${STORE_NAME}`

export const BIKES_OF_STORE             = `${BASE}/bikes`
export const BOOKINGS_OF_STORE          = `${BASE}/bookings`
export const STORE_PAGE_BY_STORE_NAME   = `${BASE}/store-page`
export const DELETE_BIKE                = `${BASE}/bikes/${ID}/delete`

export const MY_STORES                  = `${BASE}/my-stores`

export const COMMENT_BOOKING            = `${BASE}/bookings/${ID}/comment`