//Page for registering a new store
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import './StoreRegistration.css'
import StoreOpeningTimesConfig from '../../storeConfig/components/StoreOpeningTimesConfig';

import 'react-time-picker/dist/TimePicker.css';

import BikeList from '../../bikeList/components/BikeList'
import PictureAndDescriptionField from '../../../components/display/pictureAndDescriptionField/PictureAndDescriptionField';
import AddressField from '../../../components/display/addressField/AddressField';
import { useNavigate } from 'react-router-dom';
import { CREATE_STORE } from '../../../constants/URIs/AdminURIs';
import { getCookie } from '../../../services/Cookies';

const StoreRegistration = () => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    const handleCancelClick = () => {
        // TODO add a confirmation dialogue
        navigate('/stores')
    }

    const token = getCookie('token')

    const [region, setRegion] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [email, setEmail] = useState('');
    const [address, setAddress] = useState('');
    const [name, setName] = useState('');

    const handleRegionChange = () => {
        // TODO implement
    }

    const handlePhoneNumberChange = () => {
        // TODO implement
    }

    const handleEmailChange = () => {
        // TODO implement   
    }

    const handleAddressChange = (value) => {
        setAddress(value);
    }

    const handleNameChange = () => {
        // TODO implement
    }

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

    const handleRegisterClick = () => {
        postNewStore();
    }

    return (
        <>
            <h1>{t('new_store')}</h1>
            <PictureAndDescriptionField editable={true}/>
            <AddressField editable={true} onChange={handleAddressChange}/>
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