import React, { useContext, useState } from 'react';
import { useTranslation } from 'react-i18next';

import defaultBikeImage from '../../../../assets/images/default_bike.png'

import { useNavigate } from 'react-router-dom';
import { HOST, ID } from '../../../../constants/URIs/General';
import { ERR_DELETING_BIKE } from '../../../../constants/messages/ErrorMessages';
import { getCookie } from '../../../../services/Cookies'
import ConfirmationPopup from '../../../confirmationDialog/ConfirmationPopup';
import { BIKE_BOOKINGS, BIKE_CONFIG, STORE_CONFIG } from '../../../../constants/URLs/Navigation';
import { STORE_NAME } from '../../../../constants/URLs/General';
import { DELETE_BIKE as DELETE_BIKE_ADMIN  } from '../../../../constants/URIs/AdminURIs';
import { DELETE_BIKE as DELETE_BIKE_MANAGER } from '../../../../constants/URIs/ManagerURIs';
import { AuthContext } from '../../../../AuthProvider';
import { Roles } from '../../../../constants/Roles';

import { useNotification } from '../../../notifications/NotificationContext';

const BikeListItemManager = ({ bike }) => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    const { showNotification } = useNotification();

    // THINK maybe show big preview of bike image on clik on miniature preview

    const token = getCookie('token');
    const { userRoles } = useContext(AuthContext);    

    const [showDeleteConfirmation, setShowDeleteConfirmation] = useState(false);

    const handlePanelClick = () => {
        navigate(BIKE_CONFIG.replace(ID, bike.id));
    }

    const handleBookingsClick = e => {
        navigate(BIKE_BOOKINGS, { state: { id: bike.id } })
        e.stopPropagation()
    }

    const handleStoreClick = e => {
        navigate(STORE_CONFIG.replace(STORE_NAME, bike.store))
        e.stopPropagation()
    }

    const handleDeleteClick = e => {
        setShowDeleteConfirmation(true)
        e.stopPropagation()
    }

    const postBikeDeletion = () => {
        let uri = userRoles.includes(Roles.ADMINISTRATOR) ? DELETE_BIKE_ADMIN : DELETE_BIKE_MANAGER;
        uri = uri.replace(ID, bike.id)
        fetch(uri, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
            .then(response => {
                if (response.ok) {
                    console.log(t('bike_deleted_successfully'));
                    window.location.reload();
                } else {
                    return response.json().then((errorText) => {
                        throw new Error(errorText.detail);
                    });
                }
            })
            .catch(error => {
                showNotification(`${ERR_DELETING_BIKE} ${error.message}`, 'error');
            })
    }

    const handleDeleteConfirm = () => {
        postBikeDeletion();
        setShowDeleteConfirmation(false)
    }

    const handleDeleteCancel = () => {
        setShowDeleteConfirmation(false)
    }

    return (
        <>
            <li className='list-item' onClick={handlePanelClick}>

                <p className='list-item-label'>{bike.name}</p>

                <button type='button' className='list-item-button regular' onClick={handleBookingsClick}>{t('bookings')}</button>
                <button type='button' className='list-item-button regular' onClick={handleStoreClick}>{t('store')}</button>
                <button type='button' className='list-item-button accent' onClick={handleDeleteClick}>{t('delete')}</button>

                <div className='list-item-img-container'>
                    <img className='list-item-img' alt={bike.name} src={bike.image ? HOST + bike.image : defaultBikeImage}></img>
                </div>
            </li>

            <ConfirmationPopup onConfirm={handleDeleteConfirm} onCancel={handleDeleteCancel} show={showDeleteConfirmation}>
                {t('are_you_sure_you_want_to_delete_bike') + ' ' + bike.name + '?'}
            </ConfirmationPopup>
        </>
    );
};

export default BikeListItemManager;