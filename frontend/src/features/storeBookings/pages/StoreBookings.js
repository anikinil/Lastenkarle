import React from "react"
import { useLocation } from "react-router-dom";
import BookingList from "../../bookingList/pages/BookingList";


const StoreBookings = () => {

    const storeName = useLocation().state.storeName

    return (
        <>
            <h1>{t('bookings_of_store')} {storeName}</h1>

            <BookingList />
        </>
    )
}

export default StoreBookings;