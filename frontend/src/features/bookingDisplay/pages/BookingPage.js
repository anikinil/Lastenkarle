import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import { useNavigate } from 'react-router-dom';

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
            <h1>{t('booking')} {booking.id}</h1>

            <p>{booking.date}</p>
            <p>{booking.status}</p>
            <p>{booking.store.name}</p>
            <p>{booking.bike.name}</p>
            <li className='list-item'>{booking.user.name}</li>
            <li className='list-item'>
                {booking.equipment?.map(e =>
                    <p>{e}</p>
                )}
            </li>
            <p>{booking.comment}</p>

            <div className='button-container'>
                <button type='button' className='button accent' onClick={null}>{t('register')}</button>
            </div>
        </>
    );
};

export default BookingPage;