//Item or Store in List of stores
import React from 'react';
import { useTranslation } from 'react-i18next';

import { useNavigate } from 'react-router-dom';

import { MdDelete } from 'react-icons/md';

import defaultStorePicture from '../../../assets/images/default_bike.png'

const StoreListItem = ({ store }) => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    const handlePanelClick = () => {
        // use proper identifier
        navigate(`/store/${store.id}`)
    }

    const handleBookingsClick = e => {
        // TODO implement
        console.log('bookings')
        e.stopPropagation()
    }

    const handleDeleteClick = e => {
        // TODO implement
        console.log('delete')
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