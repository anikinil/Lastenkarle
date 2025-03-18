//item of BookingList
import React from 'react';

import { useTranslation } from 'react-i18next';

import defaultBikeImage from '../../../../assets/images/default_bike.png';
import { useNavigate } from 'react-router-dom';
import { HOST } from '../../../../constants/URIs/General';
import { BIKE_CONFIG, BOOKING_PAGE } from '../../../../constants/URLs/Navigation';
import { ID } from '../../../../constants/URLs/General';
import { BIKE_BY_ID } from '../../../../constants/URIs/RentingURIs';
import { getCookie } from '../../../../services/Cookies';
import { ERR_FETCHING_BIKE } from '../../../../constants/ErrorMessages';
import { useState } from 'react';
import { useEffect } from 'react';

const BookingListItem = ({ booking }) => {

    const { t } = useTranslation();

    const navigate = useNavigate()

    const token = getCookie('token')


    const [bikeName, setBikeName] = useState('');
    const [bikeImage, setBikeImage] = useState(null);


    const handlePanelClick = () => {
        navigate(BOOKING_PAGE.replace(ID, booking.id))
    }

    const handleBikeClick = e => {
        navigate(BIKE_CONFIG.replace(ID, booking.bike));
        e.stopPropagation();
    }

    // fetches bike data
    const fetchBike = () => {
        fetch(BIKE_BY_ID.replace(ID, booking.bike), {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
            .then(response => response.json())
            .then(bike => {
                setBikeName(bike.name);
                setBikeImage(bike.image);
            })
            .catch(error => {
                console.error(ERR_FETCHING_BIKE, error);
            });
    }

    useEffect(() => {
        fetchBike();
    }, [])

    const getBookingStatusString = () => {
        return booking.booking_status.map(status => status.status).join(', ')
    }

    return (
        <li className='list-item' onClick={handlePanelClick}>

            <p className='list-item-label'>{t('user')}: {booking.user.username}</p>
            <p className='list-item-label'>{t('status')}: {getBookingStatusString()}</p>
            <p className='list-item-label'>{t('from')}: {booking.begin}</p>
            <p className='list-item-label'>{t('to')}: {booking.begin}</p>

            <button type='button' className='list-item-button regular' onClick={handleBikeClick}>{bikeName}</button>

            <div className='list-item-img-container'>
                <img className='list-item-img' alt={bikeName} src={bikeImage ? HOST + bikeImage : defaultBikeImage}></img>
            </div>
        </li>
    );
};

export default BookingListItem;