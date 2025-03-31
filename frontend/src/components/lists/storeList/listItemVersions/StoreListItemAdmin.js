
//Item or Store in List of stores
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import defaultStoreImage from '../../../../assets/images/default_store.png';
import { STORE_NAME } from '../../../../constants/URLs/General';
import { STORE_CONFIG } from '../../../../constants/URLs/Navigation';
import ConfirmationPopup from '../../../confirmationDialog/ConfirmationPopup';
import { DELETE_STORE } from '../../../../constants/URIs/AdminURIs';
import { ERR_DELETING_STORE } from '../../../../constants/messages/ErrorMessages';
import { getCookie } from '../../../../services/Cookies';
import { useTranslation } from 'react-i18next';
import { HOST } from '../../../../constants/URIs/General';

import { useNotification } from '../../../notifications/NotificationContext';

const StoreListItemAdmin = ({ store }) => {

    const { t } = useTranslation();
    const { showNotification } = useNotification();
    const navigate = useNavigate();
    const token = getCookie('token');

    const [showConfirmationPopup, setShowConfirmationPopup] = useState(false);

    const handlePanelClick = () => {
        navigate(STORE_CONFIG.replace(STORE_NAME, store.name));
    }

    const handleDeleteClick = e => {
        setShowConfirmationPopup(true)
        e.stopPropagation()
    }

    // TODO needs also to account for the case when the user is not an admin
    const postBikeDeletion = () => {

        const payload = {}

        fetch(DELETE_STORE.replace(STORE_NAME, store.name), {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                if (response.ok) {
                    setShowConfirmationPopup(false);
                    window.location.reload();
                }
                else {
                    return response.json().then((errorText) => {
                        throw new Error(errorText.detail);
                    });
                }
            })
            .catch(error => {
                setShowConfirmationPopup(false);
                showNotification(`${ERR_DELETING_STORE} ${error.message}`, 'error');
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
                <p className='list-item-label'>{store.name}</p>
                <p className='list-item-label'>{store.address}</p>
                <button type='button' className='list-item-button accent' onClick={handleDeleteClick}>{t('delete')}</button>
                <div className='list-item-img-container'>
                    <img className='list-item-img' alt={store.name} src={store.image ? HOST + store.image : defaultStoreImage}></img>
                </div>
            </li>

            <ConfirmationPopup onConfirm={handlePopupConfirm} onCancel={handlePopupCancel} show={showConfirmationPopup}>
                {t('are_you_sure_you_want_to_delete_store') + ' ' + store.name + '?'}
            </ConfirmationPopup>
        </>
    );
};

export default StoreListItemAdmin;
