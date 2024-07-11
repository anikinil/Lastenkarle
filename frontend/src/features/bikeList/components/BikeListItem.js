import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css'

import { MdDelete } from 'react-icons/md';

import defaultBikePicture from '../../../assets/images/default_bike.png'

import { useNavigate } from 'react-router-dom';
import ConfirmationPopup from '../../../components/confirmationDialogue/ConfirmationPopup';

const BikeListItem = ({ bike }) => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    // THINK how to display different buttons to different roles
    // THINK maybe show big preview of bike image on clik on miniature preview

    const [showConfirmationPopup, setShowConfirmationPopup] = useState(false);

    const handlePanelClick = () => {
        navigate(`/bike/${bike.id}`);
    }

    const handleBookingsClick = e => {
        // TODO implement
        console.log('bookings')
        e.stopPropagation()
    }

    const handleStoreClick = e => {
        navigate(`/store/${bike.storeId}`)
        e.stopPropagation()
    }

    const handleDeleteClick = e => {
        // TODO implement
        setShowConfirmationPopup(true)
        e.stopPropagation()
    }

    const handlePopupConfirm = () => {
        // TODO implement deletion
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
                    {/* TODO make proper string insertion */}
                    {`t('are_you_sure_you_want_to_delete_this_bike')${bike.name}`}
            </ConfirmationPopup>
        </>
    );
};

export default BikeListItem;