import React from 'react';

import { useTranslation } from 'react-i18next';

import defaultBikePicture from '../../../assets/images/default_bike.png'
import { useNavigate } from 'react-router-dom';

const BookingListItem = ({ booking }) => {

    const { t } = useTranslation();

    const navigate = useNavigate()

    // THINK make a seperate booking page?
    const handlePanelClick = () => {
        console.log(booking.bike.name)
    }

    const handleStoreClick = e => {
        navigate('/store/' + booking.store.id)
        e.stopPropagation()
    }

    const handleUserClick = e => {
        // TODO implement user page
        navigate('/user/' + booking.user.id)
        e.stopPropagation()
    }

    return (
        <li className='list-item' onClick={handlePanelClick}>

            <p className='list-item-label'>{booking.date}</p>
            <p className='list-item-label'>{booking.bike.name}</p>
            <p className='list-item-label'>{booking.status}</p>

            <button type='button' className='list-item-button regular' onClick={handleStoreClick}>{booking.store.name}</button>
            <button type='button' className='list-item-button regular' onClick={handleUserClick}>{booking.user.name}</button>

            <div className='list-item-img-container'>
                <img className='list-item-img' alt={booking.bike.name} src={booking.bike.image ? booking.bike.image : defaultBikePicture}></img>
            </div>
        </li>
    );
};

export default BookingListItem;