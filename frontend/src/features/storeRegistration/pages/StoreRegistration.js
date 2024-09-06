import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import './StoreRegistration.css'
import StoreOpeningTimesConfig from '../../storeConfig/components/StoreOpeningTimesConfig';

import 'react-time-picker/dist/TimePicker.css';

import BikeList from '../../bikeList/components/BikeList'
import PictureAndDescriptionField from '../../../components/display/pictureAndDescriptionField/PictureAndDescriptionField';
import AddressField from '../../../components/display/addressField/AddressField';
import { useNavigate } from 'react-router-dom';

const StoreRegistration = () => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    const handleCancelClick = () => {
        // TODO maybe add a confirmation dialogue
        navigate('/stores')
    }

    const handleRegisterClick = () => {
        // TODO implement
    }

    return (
        <>
            <h1>{t('new_store')}</h1>
            <PictureAndDescriptionField editable={true}/>
            <AddressField editable={true}/>
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