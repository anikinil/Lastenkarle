import React from 'react';
import { useTranslation } from 'react-i18next';

import './BikeRegistration.css'
import PictureAndDescriptionField from '../../../components/display/pictureAndDescriptionField/PictureAndDescriptionField';
import { useNavigate } from 'react-router-dom';
import { BIKES } from '../../../constants/URLs/Navigation';
import { ERR_POSTING_NEW_BIKE } from '../../../constants/ErrorMessages';
import { getCookie } from '../../../services/Cookies';

const BikeRegistration = () => {
    // Hook for translation
    const { t } = useTranslation();

    // Hook for navigation
    const navigate = useNavigate()

    const token = getCookie('token') // Get authentication token

    // Handler for cancel button click
    const handleCancelClick = () => {
        // TODO maybe add a confirmation dialogue
        navigate(-1)
    }

    const postNewBike = () => {
        let payload = {
            
        };
        // TODO add URI
        return fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                if (response.ok) {
                    alert(t('bike_registration_successful'));
                    navigate(-1);
                } else {
                    return response.json().then((errorText) => {
                        throw new Error(errorText.detail);
                    });
                }
            })
            .catch(error => {
                alert(ERR_POSTING_NEW_BIKE + ' ' + error.message);
            });
    }

    // Handler for register button click
    const handleRegisterClick = () => {
        postNewBike();
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