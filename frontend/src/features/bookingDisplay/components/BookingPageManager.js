import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { useNavigate, useParams } from 'react-router-dom';
import { SELECTED_BOOKING } from '../../../constants/URIs/AdminURIs';
import { ERR_FETCHING_BIKE, ERR_FETCHING_BOOKING, ERR_UPDATING_COMMENT } from '../../../constants/messages/ErrorMessages';
import { ID } from '../../../constants/URIs/General';
import { getCookie } from '../../../services/Cookies';
import { BIKE_CONFIG } from '../../../constants/URLs/Navigation';
import { BIKE_BY_ID } from '../../../constants/URIs/RentingURIs';

import defaultBikeImage from '../../../assets/images/default_bike.png';
import { HOST } from '../../../constants/URIs/General';
import TextField from '../../../components/display/TextField';
import { COMMENT_BOOKING } from '../../../constants/URIs/ManagerURIs';
import { useNotification } from '../../../components/notifications/NotificationContext';

// Displays a single booking without the option of editing.
const BookingPageManager = () => {

    const { t } = useTranslation();

    const { showNotification } = useNotification();

    const bookingId = useParams().id;

    const navigate = useNavigate();

    const [booking, setBooking] = useState({});
    const [bike, setBike] = useState({});
    const [comment, setComment] = useState('');
    const [newComment, setNewComment] = useState('');

    const token = getCookie('token');

    const fetchBooking = () => {
        // console.log(SELECTED_BOOKING.replace(ID, bookingId))
        fetch(SELECTED_BOOKING.replace(ID, bookingId), {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
            .then(response => response.json())
            .then(data => {
                setBooking(data);
                setComment(data.comment);
                console.log(data);
                fetchBike(data.bike);
            })
            .catch(error => {
                console.error(ERR_FETCHING_BOOKING, error);
            });
    }

    // fetches bike data
    const fetchBike = (bikeId) => {
        fetch(BIKE_BY_ID.replace(ID, bikeId), {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
            .then(response => response.json())
            .then(data => {
                setBike(data);
                console.log(data);
            })
            .catch(error => {
                console.error(ERR_FETCHING_BIKE, error);
            });
    }

    useEffect(() => {
        fetchBooking();
    }, [])

    const getBookingStatusString = () => {
        return booking.booking_status.map(status => status.status).join(', ')
    }

    const handleCommentChange = (value) => {
        setNewComment(value);
    }

    const handleSaveChangesClick = () => {
        let payload = {
            comment: newComment
        };
        return fetch(COMMENT_BOOKING.replace(ID, bookingId), {
            method: 'PATCH',
            headers: {
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify(payload)

        })
            .then(response => {
                if (response.ok) {
                    showNotification(t('comment_update_successful'), 'success');
                    navigate(-1);
                } else {
                    return response.json().then((errorText) => {
                        throw new Error(errorText.detail);
                    });
                }
            })
            .catch(error => {
                showNotification(`${ERR_UPDATING_COMMENT} ${error.message}`, 'error');
            });
    }

    const handleCancelClick = () => {
        navigate(-1);
    }

    return (
        <>
            {/* TODO format properly */}
            <h1>{t('booking')} {booking?.id}: {booking?.begin} - {booking?.end}</h1>

            <a href={BIKE_CONFIG.replace(ID, bike?.id)}>{bike?.name}</a>

            <div className='list-item-img-container'>
                <img className='list-item-img' alt={bike?.name} src={bike?.image ? HOST + bike?.image : defaultBikeImage}></img>
            </div>

            {booking?.booking_status && <p>{t('status')}: {getBookingStatusString()}</p>}

            <p>{t('user')}: {booking?.user?.username}</p>

            {booking?.bike_equipment?.length > 0 &&
                <p>{t('equipment')}: {booking?.equipment?.map(e => e).join(', ')}</p>
            }

            <h2>{'comment'}</h2>
            <TextField title={t('comment')} placeholder={t('no_comment')} editable={true} singleLine={false} value={comment} handleChange={handleCommentChange} />
            <div className='button-container'>
                <button type='button' className='button accent' onClick={handleSaveChangesClick}>{t('save_changes')}</button>
                <button type='button' className='button regular' onClick={handleCancelClick}>{t('cancel')}</button>
            </div>
        </>
    );
};

export default BookingPageManager;