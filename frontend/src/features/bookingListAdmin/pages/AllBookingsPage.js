//Intended to be a component
//List of bookings
import React, { useState, useEffect } from 'react';

import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css';

import { ALL_BOOKINGS } from '../../../constants/URIs/AdminURIs';
import BookingListAdmin from '../../../components/lists/bookingList/listVersions/BookingListAdmin';
import { getCookie } from '../../../services/Cookies';

const AllBookingsPage = () => {

    const { t } = useTranslation();

    const token = getCookie('token');

    const [bookings, setBookings] = useState([])

    const fetchBookings = async () => {
        const response = await fetch(ALL_BOOKINGS, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
            }
        });
        const data = await response.json();
        setBookings(data);
    };

    useEffect(() => {
        fetchBookings();
    }, [])


    return (
        <>
            <h1>{t('bookings')}</h1>
            <BookingListAdmin bookings={bookings} />
        </>
    );
};

export default AllBookingsPage;