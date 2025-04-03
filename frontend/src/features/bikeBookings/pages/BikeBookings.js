import React from "react";
import { useLocation } from "react-router-dom";
import BookingList from "../../allBookings/pages/AllBookingsPage";
import { useTranslation } from "react-i18next";

// Page component for displaying the bookings of a store
const BikeBookings = () => {
    // Use the useTranslation hook to get the translation function
    const { t } = useTranslation();

    // Get the storeName from the location state
    const storeName = useLocation().state.storeName;

    return (
        <>
            {/* Display the translated heading with the store name */}
            <h1>{t('bookings_of_store')} {storeName}</h1>

            {/* Render the BookingList component */}
            <BookingList />
        </>
    );
}

export default BikeBookings;