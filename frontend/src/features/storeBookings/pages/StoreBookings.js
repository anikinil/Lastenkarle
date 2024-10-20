import React from "react"
import { useLocation } from "react-router-dom";
import BookingList from "../../bookingList/pages/BookingList";
import { useTranslation } from "react-i18next";

const StoreBookings = () => {

    const { t } = useTranslation()

    const storeName = useLocation().state.storeName

    return (
        <>
            <h1>{t('bookings_of_store')} {storeName}</h1>

            <BookingList />
        </>
    )
}

export default StoreBookings;