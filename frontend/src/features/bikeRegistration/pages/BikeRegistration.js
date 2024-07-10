import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import './BikeRegistration.css'
import PictureAndDescriptionField from '../../../components/IO/PictureAndDescriptionField';
import { useNavigate } from 'react-router-dom';

const BikeRegistration = () => {

    const { t } = useTranslation();

    const navigate = useNavigate()

    const handleCancelClick = () => {
        // TODO maybe add a confirmation dialogue
        navigate('/bikes')
    }

    const handleRegisterClick = () => {
        // TODO implement
    }

    return (
        <>
            <h1>{t('new_bike')}</h1>

            <PictureAndDescriptionField editable={true}/>

            <div className='button-container'>
                <button type='button' className='button' onClick={handleCancelClick}>{t('cancel')}</button>
                <button type='button' className='button register' onClick={handleRegisterClick}>{t('register_new_bike')}</button>
            </div>
        </>
    );
};

export default BikeRegistration;