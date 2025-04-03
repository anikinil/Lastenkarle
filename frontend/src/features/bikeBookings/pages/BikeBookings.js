import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";
import BookingList from "../../../components/lists/bookingList/BookingList";
import { BIKE_BOOKINGS } from "../../../constants/URLs/Navigation";
import { ID } from "../../../constants/URIs/General";
import { getCookie } from "../../../services/Cookies";
import { BIKE_BY_ID } from "../../../constants/URIs/RentingURIs";
import { ERR_FETCHING_BIKE } from "../../../constants/messages/ErrorMessages";

// Page component for displaying the bookings of a store
const BikeBookings = () => {
    // Use the useTranslation hook to get the translation function
    const { t } = useTranslation();

    const token = getCookie('token');

    // Get the storeName from the location state
    const bikeId = useLocation().state.id;

    const [bike, setBike] = useState();
    const [bookings, setBookings] = useState([])

    const fetchBike = () => {
        fetch(BIKE_BY_ID.replace(ID, bikeId), {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
            .then(response => response.json())
            .then(bike => {
                setBike(bike);
            })
            .catch(error => {
                console.error(ERR_FETCHING_BIKE, error);
            });
    }

    const fetchBookings = async () => {
        const response = await fetch(BIKE_BOOKINGS.replace(ID, bikeId), {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
            }
        });
        const data = await response.json();
        setBookings(data);
    };

    useEffect(() => {
        fetchBike();
        fetchBookings();
    }, [])


    return (
        <>
            {/* Display the translated heading with the store name */}
            <h1>{t('bookings_of_bike')} {bike.name}</h1>

            {/* Render the BookingList component */}
            <BookingList bookings={bookings} />
        </>
    );
}

export default BikeBookings;