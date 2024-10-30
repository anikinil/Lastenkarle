//Item or Store in List of stores
import React from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { MdDelete } from 'react-icons/md';

import defaultStorePicture from '../../../assets/images/default_bike.png'
import { STORE_BY_BIKE_ID } from '../../../constants/URIs/BookingURIs';
import { STORE_NAME } from '../../../constants/URIs/ManagerURI';
import { DELETE_STORE } from '../../../constants/URIs/AdminURIs';
import { getCookie } from '../../../services/Cookies';
import { ERR_DELETING_STORE } from '../../../constants/ErrorMessages';
import { ID } from '../../../constants/URIs/General';
import { BOOKINGS } from '../../../constants/URLs/Navigation';

const StoreListItem = ({ store }) => {
    const { t } = useTranslation();
    const navigate = useNavigate();
    const token = getCookie('token');

    // Function to handle store deletion
    const postStoreDeletion = () => {
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
                if (response) {
                    alert(t('enrollment_successful'));
                } else {
                    return response.json().then((errorText) => {
                        throw new Error(errorText.detail);
                    });
                }
            })
            .catch(error => {
                alert(ERR_DELETING_STORE + ' ' + error.message);
            })
    }

    // Function to handle panel click and navigate to store details
    const handlePanelClick = () => {
        navigate(STORE_BY_BIKE_ID.replace(ID, store.id));
    }

    // Function to handle bookings button click and navigate to bookings page
    const handleBookingsClick = e => {
        navigate(BOOKINGS, { state: { filterStore: store } })
        e.stopPropagation()
    }

    // Function to handle delete button click and delete the store
    const handleDeleteClick = e => {
        // TODO add confirmation dialog
        postStoreDeletion()
        e.stopPropagation()
    }

    return (
        <li className='list-item' onClick={handlePanelClick}>
            <p className='list-item-label'>{store.name}</p>
            <button type='button' className='list-item-button regular' onClick={handleBookingsClick}>{t('bookings')}</button>
            <button type='button' className='list-item-button delete' onClick={handleDeleteClick}>{<MdDelete />}</button>
            <div className='list-item-img-container'>
                <img className='list-item-img' alt={store.name} src={store.image ? store.image : defaultStorePicture}></img>
            </div>
        </li>
    );
};

export default StoreListItem;
