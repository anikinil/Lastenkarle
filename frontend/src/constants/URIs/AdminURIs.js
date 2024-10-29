import { HOST } from "./General"

const BASE = `${HOST}/api/admin/v1`

export const ALL_EQUIPMENT                  = `${BASE}/equipment`
export const USER_FLAGS                     = `${BASE}/user-flags`
export const ALL_USERS                      = `${BASE}/users`
export const SELECTED_USER                  = `${BASE}/users/{USER_ID}`
export const BOOKINGS_OF_SELECTED_USERS     = `${SELECTED_USER}/bookings`
export const BAN_USER                       = `${BASE}/ban-user`
export const ALL_BOOKINGS                   = `${BASE}/bookings`
export const SELECTED_BOOKING               = `${BASE}/bookings/{BOOKING_ID}`
export const ADD_BIKE_TO_STORE              = `${BASE}/create/store/{STORE_ID}/bike`
export const DELETE_BIKE                    = `${BASE}/delete/bike/{BIKE_ID}`
export const ALL_BIKES                      = `${BASE}/bikes`
export const ALL_STORES                     = `${BASE}/stores`

export const CREATE_STORE                   = `${BASE}/create/store`