import { HOST, ID } from "./General";

const BASE = `${HOST}/api/booking/v1`

export const BIKE_BY_ID       = `${BASE}/bikes/${ID}`
export const STORE_BY_BIKE_ID = `${BASE}/bikes/${ID}/store`
export const ALL_STORES       = `${BASE}/stores`
export const REGIONS          = `${BASE}/region`