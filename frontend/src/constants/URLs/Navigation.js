// TODO replace everywhere by these variables

import { ID, KEY } from "./General"
import { STORE_NAME, REGION_NAME } from "./General"

export const HOME                   = `/`

// TODO replace by correct URL
export const HELMHOLTZ              = `/HELMHOLTZ`

export const LOGIN                  = `/login`
export const LOGOUT                 = `/logout`
export const ACCOUNT_DELETION       = `/account-deletion`
export const REGISTER               = `/register`
export const ENROLLMENT             = `/enrollment`
export const USER_BAN               = `/user-ban`
export const BOOKING_PAGE           = `/booking/${ID}`
export const USERS                  = `/users`
export const NO_PERMISSION          = `/no-permission`
export const BIKE_BOOKING           = `/bike-booking`
export const BIKES                  = `/bikes`
export const BIKE                   = `/bike/${ID}`
export const BIKE_REGISTRATION      = `/store/${STORE_NAME}/bike-registration`
export const STORES                 = `/stores`
export const STORE                  = `/store/${STORE_NAME}`
export const STORE_REGISTRATION     = `/store-registration`
export const BOOKINGS               = `/bookings`
export const STORE_BOOKINGS         = `${STORE}/store-bookings`

export const BOOKING                = `/booking`
export const REGIONAL_BOOKING       = `/regional-booking/${REGION_NAME}`

export const EMAIL_VERIFICATION     = `/email-verification/${ID}/${KEY}`