import { HOST } from "../URIs/General"
import { ID, KEY } from "./General"
import { STORE_NAME, REGION_NAME } from "./General"

export const HOME                   = `/`
export const NO_PERMISSION          = `/no-permission`

// TODO check if correct
export const HELMHOLTZ              = `${HOST}/api/user/v1/helmholtz/login`

export const LOGIN                  = `/login`
export const LOGOUT                 = `/logout`
export const ACCOUNT_DELETION       = `/account-deletion`
export const REGISTER               = `/register`

export const ENROLLMENT             = `/enrollment`
export const USER_BAN               = `/user-ban`
export const ALL_USERS              = `/all-users`
export const USER_PAGE              = `/user/${ID}`

export const ALL_STORES             = `/all-stores`                              // all stores in the system (admin)
export const MY_STORES              = `/my-stores`                               // stores of particular in manager (manager, admin)
export const STORE_PAGE_OF_BIKE     = `/store-page-of-bike/${ID}`                // display store page of a particular bike (customer)
export const STORE_DISPLAY          = `/store-page/${ID}`                        // display store page (customer)
export const STORE_CONFIG           = `/store-config/${STORE_NAME}`              // configure store (manager, admin)
export const STORE_REGISTRATION     = `/store-registration`                      // register store (admin)

export const ALL_BIKES              = `/all-bikes`                               // all bikes in the system (admin)
export const BIKE                   = `/bike/${ID}`
export const STORE_BIKES            = `/store/${STORE_NAME}/store-bikes`         // all bikes in a store
export const BIKE_CONFIG            = `/bike-config/${ID}`                       // configure bike (manager, admin)
export const BIKE_REGISTRATION      = `/store/${STORE_NAME}/bike-registration`   // register bike (manager, admin)

export const ALL_BOOKINGS           = `/all-bookings`
export const MY_BOOKINGS            = `/my-bookings`
export const BOOKING_PAGE           = `/booking/${ID}`
export const STORE_BOOKINGS         = `/store/${STORE_NAME}/store-bookings`

export const RENTING                = `/renting`
export const REGIONAL_RENTING       = `/regional-renting/${REGION_NAME}`
export const BIKE_RENTING           = `/bike-renting/${ID}`

export const EMAIL_VERIFICATION     = `/email-verification/${ID}/${KEY}`