import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import { useNavigate } from 'react-router-dom';
import StoreListItem from '../../storeList/components/StoreListItem';
import BikeListItem from '../../bikeList/components/BikeListItem';
import DisplayPanel from '../../../components/display/DisplayPanel';

// TODO ! make every list a seperate component, so e. g. a bike list can be displayed inside store page 

const BookingPage = () => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    const booking = {
        id: 3,
        date: '12.05.2024',
        status: 'booked',
        store: {
            id: 3,
            name: 'Store3'
        },
        bike: {
            id: 1,
            name: 'Lastenrad 1',
            image: require('../../../assets/images/bike1.jpg')
        },
        user: {
            id: 3,
            name: 'alma42'
        },
        equipment: ["Gürtel", "Helm", "Kind"],
        comment: "suspicious activities"
    }


    return (
        <>
            <h1>{t('booking')} {booking.id} - {booking.date} - {booking.status}</h1>

            <DisplayPanel content={<p>{booking.store.name}</p>} handleClick={() => navigate(`/store/${booking.store.id}`)} />
            <DisplayPanel content={<p>{booking.bike.name}</p>} handleClick={() => navigate(`/bike/${booking.bike.id}`)} />
            <DisplayPanel content={<p>{booking.user.name}</p>} />
            <DisplayPanel content={booking.equipment?.map(e => <label>{e}</label>)} />

            <DisplayPanel content={<p>{booking.comment}</p>} />
        </>
    );
};

export default BookingPage;