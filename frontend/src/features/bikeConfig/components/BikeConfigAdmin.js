import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import PictureAndDescriptionField from '../../../components/display/pictureAndDescriptionField/PictureAndDescriptionField';
import { useNavigate, useParams } from 'react-router-dom';
import { ERR_POSTING_NEW_BIKE } from '../../../constants/ErrorMessages';
import { getCookie } from '../../../services/Cookies';
import { BIKES_OF_STORE, STORE_NAME } from '../../../constants/URIs/ManagerURIs';
import SingleLineTextField from '../../../components/display/SingleLineTextField';

const BikeConfigAdmin = () => {
    // Hook for translation
    const { t } = useTranslation();

    // Hook for navigation
    const navigate = useNavigate()

    const storeName = useParams().store;

    const token = getCookie('token') // Get authentication token

    const [name, setName] = useState('');
    const [pictureFile, setPictureFile] = useState(null);
    const [description, setDescription] = useState('');

    // Handler for cancel button click
    const handleCancelClick = () => {
        // TODO maybe add a confirmation dialog
        navigate(-1)
    }

    const postNewBike = () => {
        const formData = new FormData();
        formData.append("name", name);
        formData.append("description", description);
        formData.append("image", pictureFile);
        return fetch(BIKES_OF_STORE.replace(STORE_NAME, storeName), {
            method: 'POST',
            headers: {
                'Authorization': `Token ${token}`
            },
            body: formData
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

    const handleNameChange = (value) => {
        setName(value)
    }

    const handlePictureChange = (value) => {
        setPictureFile(value)
    }

    const handleDescriptionChange = (value) => {
        setDescription(value)
    }

    // Handler for register button click
    const handleRegisterClick = () => {
        postNewBike();
    }

    return (
        <>
            {/* Page title */}
            <h1>{t('new_bike_to')} {storeName}</h1>

            <SingleLineTextField title={t('name')} editable={true} onChange={handleNameChange} />

            {/* Picture and description field component */}
            <PictureAndDescriptionField editable={true} onPictureChange={handlePictureChange} onDescriptionChange={handleDescriptionChange}/>

            {/* Button container */}
            <div className='button-container'>
                <button type='button' className='button' onClick={handleCancelClick}>{t('cancel')}</button>
                <button type='button' className='button register' onClick={handleRegisterClick}>{t('register_new_bike')}</button>
            </div>
        </>
    );
};

export default BikeConfigAdmin;