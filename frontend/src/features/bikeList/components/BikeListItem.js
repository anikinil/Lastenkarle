import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css'

import { MdDelete } from 'react-icons/md';

import defaultBikePicture from '../../../assets/images/default_bike.png'

import { useNavigate } from 'react-router-dom';
import ConfirmationPopup from '../../../components/confirmationDialog/ConfirmationPopup';
import { BIKE, BOOKINGS } from '../../../constants/URLs/Navigation';
import { ID } from '../../../constants/URIs/General';
import { STORE_BY_BIKE_ID } from '../../../constants/URIs/BookingURIs';
import { DELETE_BIKE } from '../../../constants/URIs/AdminURIs';
import { ERR_DELETING_BIKE } from '../../../constants/ErrorMessages';

const BikeListItem = ({ bike }) => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    // THINK how to display different buttons to different roles
    // THINK maybe show big preview of bike image on clik on miniature preview

    const [showConfirmationPopup, setShowConfirmationPopup] = useState(false);

    const handlePanelClick = () => {
        navigate(BIKE.replace(ID, bike.id));
    }

    const handleBookingsClick = e => {
        navigate(BOOKINGS, { state: { filterBike: bike } })
        e.stopPropagation()
    }

    const handleStoreClick = e => {
        navigate(STORE_BY_BIKE_ID.replace(ID, bike.id))
        e.stopPropagation()
    }

    const handleDeleteClick = e => {
        setShowConfirmationPopup(true)
        e.stopPropagation()
    }

    // TODO needs also to account for the case when the user is not an admin
    const postBikeDeletion = () => {

        fetch(DELETE_BIKE.replace(ID, bike.id), {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                if (response) {
                    alert(t('enrollment_successful'));
                }
                else {
                    return response.json().then((errorText) => {
                        throw new Error(errorText.detail);
                    });
                }
            })
            .catch(error => {
                alert(ERR_DELETING_BIKE + ' ' + error.message);
            })
    }

    const handlePopupConfirm = () => {
        postBikeDeletion();
    }

    const handlePopupCancel = () => {
        setShowConfirmationPopup(false)
    }

    return (
        <>
            <li className='list-item' onClick={handlePanelClick}>

                <p className='list-item-label'>{bike.name}</p>

                <button type='button' className='list-item-button regular' onClick={handleBookingsClick}>{t('bookings')}</button>
                <button type='button' className='list-item-button regular' onClick={handleStoreClick}>{t('store')}</button>
                <button type='button' className='list-item-button delete' onClick={handleDeleteClick}>{<MdDelete />}</button>

                <div className='list-item-img-container'>
                    <img className='list-item-img' alt={bike.name} src={bike.image ? bike.image : defaultBikePicture}></img>
                </div>
            </li>

            <ConfirmationPopup onConfirm={handlePopupConfirm} onCancel={handlePopupCancel} show={showConfirmationPopup}>
                {t('are_you_sure_you_want_to_delete_bike') + ' ' + bike.name + '?'}
            </ConfirmationPopup>
        </>
    );
};

export default BikeListItem;