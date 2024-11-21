// TODO replace everywhere by these variables

import { ID, KEY } from "./General"
import { STORE_NAME, REGION_NAME } from "./General"

export const HOME                   = `/`
export const NO_PERMISSION          = `/no-permission`

// TODO replace by correct URL
export const HELMHOLTZ              = `/HELMHOLTZ`

export const LOGIN                  = `/login`
export const LOGOUT                 = `/logout`
export const ACCOUNT_DELETION       = `/account-deletion`
export const REGISTER               = `/register`

export const ENROLLMENT             = `/enrollment`
export const USER_BAN               = `/user-ban`
export const USERS                  = `/users`

export const ALL_BIKES              = `/all-bikes`                               // all bikes in the system (admin)
export const BIKE                   = `/bike/${ID}`
export const STORE_BIKES            = `/store/${STORE_NAME}/store-bikes`         // all bikes in a store
export const BIKE_CONFIG            = `` // TODO add
export const BIKE_REGISTRATION      = `/store/${STORE_NAME}/bike-registration`

export const ALL_STORES             = `/all-stores`                              // all stores in the system (admin)
export const MY_STORES              = `/my-stores`                               // stores of particular in manager (manager, admin)
export const STORE_DISPLAY          = `/bike/${ID}/store`                        // display store (customer)
export const STORE_CONFIG           = `/store-config/${STORE_NAME}`              // configure store (manager, admin)
export const STORE_REGISTRATION     = `/store-registration`                      // register store (admin)

export const BOOKINGS               = `/bookings`
export const BOOKING_PAGE           = `/booking/${ID}`
export const STORE_BOOKINGS         = `/store/${STORE_NAME}/store-bookings`

export const BOOKING                = `/booking`
export const REGIONAL_BOOKING       = `/regional-booking/${REGION_NAME}`
export const BIKE_BOOKING           = `/bike-booking/${ID}`

export const EMAIL_VERIFICATION     = `/email-verification/${ID}/${KEY}`