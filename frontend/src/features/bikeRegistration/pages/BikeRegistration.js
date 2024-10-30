import React from 'react';
import { useTranslation } from 'react-i18next';

import './BikeRegistration.css'
import PictureAndDescriptionField from '../../../components/display/pictureAndDescriptionField/PictureAndDescriptionField';
import { useNavigate } from 'react-router-dom';
import { BIKES } from '../../../constants/URLs/Navigation';

const BikeRegistration = () => {
    // Hook for translation
    const { t } = useTranslation();

    // Hook for navigation
    const navigate = useNavigate()

    // Handler for cancel button click
    const handleCancelClick = () => {
        // TODO maybe add a confirmation dialogue
        navigate(BIKES)
    }

    // Handler for register button click
    const handleRegisterClick = () => {
        // TODO implement
    }

    return (
        <>
            {/* Page title */}
            <h1>{t('new_bike')}</h1>

            {/* Picture and description field component */}
            <PictureAndDescriptionField editable={true}/>

            {/* Button container */}
            <div className='button-container'>
                <button type='button' className='button' onClick={handleCancelClick}>{t('cancel')}</button>
                <button type='button' className='button register' onClick={handleRegisterClick}>{t('register_new_bike')}</button>
            </div>
        </>
    );
};

export default BikeRegistration;