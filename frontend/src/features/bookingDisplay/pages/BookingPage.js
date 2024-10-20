import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import { useLocation, useNavigate } from 'react-router-dom';
import DisplayPanel from '../../../components/display/DisplayPanel';

// TODO ! make every list a seperate component, so e. g. a bike list can be displayed inside store page 

// Displays a single booking without the option of editing.
const BookingPage = () => {

    const booking = useLocation().state.booking;

    const { t } = useTranslation();

    const navigate = useNavigate();

    return (
        <>
            <h1>{t('booking')} {booking.id} - {booking.date} - {booking.status}</h1>

            <DisplayPanel content={<p>{booking.store.name}</p>} handleClick={() => navigate(`/store/${booking.store.id}`)} />
            <DisplayPanel content={<p>{booking.bike.name}</p>} handleClick={() => navigate(`/bike/${booking.bike.id}`)} />
            <DisplayPanel content={<p>{booking.user.name}</p>} />
            <DisplayPanel content={<p>{t('equipment')}: {booking.equipment?.map(e => e).join(', ')}</p>} />
            { booking.comment ? 
            <DisplayPanel content={<p>{booking.comment}</p>} />
            :
            null}
        </>
    );
};

export default BookingPage;