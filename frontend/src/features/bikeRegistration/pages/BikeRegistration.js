import React, { useContext, useState } from 'react';
import { useTranslation } from 'react-i18next';

import './BikeRegistration.css'
import ImageAndDescriptionField from '../../../components/display/imageAndDescriptionField/ImageAndDescriptionField';
import { useNavigate, useParams } from 'react-router-dom';
import { ERR_POSTING_NEW_BIKE } from '../../../constants/ErrorMessages';
import { getCookie } from '../../../services/Cookies';
import { STORE_NAME } from '../../../constants/URIs/ManagerURIs';
import { BIKES_OF_STORE as NEW_BIKE_URI_MANAGER } from '../../../constants/URIs/ManagerURIs';
import { ADD_BIKE_TO_STORE as NEW_BIKE_URI_ADMIN } from '../../../constants/URIs/AdminURIs';
import SingleLineTextField from '../../../components/display/SingleLineTextField';
import { AuthContext } from '../../../AuthProvider';
import { Roles } from '../../../constants/Roles';

const BikeRegistration = () => {
    // Hook for translation
    const { t } = useTranslation();

    // Hook for navigation
    const navigate = useNavigate()

    const storeName = useParams().store;

    const token = getCookie('token') // Get authentication token

    const { userRoles } = useContext(AuthContext);

    const [name, setName] = useState('');
    const [imageFile, setImageFile] = useState(null);
    const [description, setDescription] = useState('');

    // Handler for cancel button click
    const handleCancelClick = () => {
        // TODO maybe add a confirmation dialog
        navigate(-1)
    }

    const postNewBike = () => {
        let uri = userRoles.includes(Roles.ADMINISTRATOR) ? NEW_BIKE_URI_ADMIN : NEW_BIKE_URI_MANAGER;
        uri = uri.replace(STORE_NAME, storeName)
        const formData = new FormData();
        formData.append("name", name);
        formData.append("description", description);
        formData.append("image", imageFile);
        return fetch(uri, {
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

    const handleImageChange = (value) => {
        setImageFile(value)
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

            {/* Image and description field component */}
            <ImageAndDescriptionField editable={true} onImageChange={handleImageChange} onDescriptionChange={handleDescriptionChange}/>

            {/* Button container */}
            <div className='button-container'>
                <button type='button' className='button' onClick={handleCancelClick}>{t('cancel')}</button>
                <button type='button' className='button register' onClick={handleRegisterClick}>{t('register_new_bike')}</button>
            </div>
        </>
    );
};

export default BikeRegistration;