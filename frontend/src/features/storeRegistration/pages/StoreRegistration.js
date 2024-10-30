// Page for registering a new store
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import './StoreRegistration.css'
import StoreOpeningTimesConfig from '../../storeConfig/components/StoreOpeningTimesConfig';

import 'react-time-picker/dist/TimePicker.css';

import BikeList from '../../bikeList/components/BikeList'
import PictureAndDescriptionField from '../../../components/display/pictureAndDescriptionField/PictureAndDescriptionField';
import SingleLineTextField from '../../../components/display/SingleLineTextField';
import { useNavigate } from 'react-router-dom';
import { CREATE_STORE } from '../../../constants/URIs/AdminURIs';
import { getCookie } from '../../../services/Cookies';

const StoreRegistration = () => {

    const { t } = useTranslation(); // Translation hook

    const navigate = useNavigate(); // Navigation hook

    const handleCancelClick = () => {
        // TODO add a confirmation dialog
        navigate('/stores') // Navigate to stores page on cancel
    }

    const token = getCookie('token') // Get authentication token

    // State variables for form fields
    const [region, setRegion] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [email, setEmail] = useState('');
    const [address, setAddress] = useState('');
    const [name, setName] = useState('');

    const handleRegionChange = () => {
        // TODO implement region change handler
    }

    // Handlers for form field changes
    const handlePhoneNumberChange = (value) => {
        setPhoneNumber(value)
    }

    const handleEmailChange = (value) => {
        setEmail(value)
    }

    const handleAddressChange = (value) => {
        setAddress(value);
    }

    const handleNameChange = (value) => {
        setName(value)
    }

    // Function to post new store data to the server
    const postNewStore = () => {

        let payload = {
            region: {name: region},
            phone_number: phoneNumber,
            email: email,
            address: address,
            name: name
        };

        return fetch(CREATE_STORE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify(payload)
        })
    }

    // Handler for register button click
    const handleRegisterClick = () => {
        postNewStore();
    }

    return (
        <>
            <h1>{t('new_store')}</h1>
            <PictureAndDescriptionField editable={true}/>

            <SingleLineTextField editable={true} title='address' onChange={handleAddressChange}/>
            <SingleLineTextField editable={true} title='phone_number' onChange={handlePhoneNumberChange}/>
            <SingleLineTextField editable={true} title='email' onChange={handleEmailChange}/>
            <SingleLineTextField editable={true} title='name' onChange={handleNameChange}/>

            <StoreOpeningTimesConfig />

            <h2>{t('add_bikes_to_store')}</h2>
            <BikeList />

            <div className='button-container'>
                <button type='button' className='button regular' onClick={handleCancelClick}>{t('cancel')}</button>
                <button type='button' className='button accent' onClick={handleRegisterClick}>{t('register_new_store')}</button>
            </div>
        </>
    );
};

export default StoreRegistration;