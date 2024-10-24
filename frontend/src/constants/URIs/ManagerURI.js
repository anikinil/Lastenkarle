import { HOST } from "./General";

const BASE = `${HOST}/api/manager/v1/${STORE_NAME}`

export const STORE_NAME = `{STORE_NAME}`

export const BIKES_OF_STORE = `${BASE}/bikes`
export const BOOKINGS_OF_STORE = `${BASE}/bookings`
export const STORE_PAGE_BY_STORE_NAME = `${BASE}/store-page`