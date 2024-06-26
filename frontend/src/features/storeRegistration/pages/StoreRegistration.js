import React, { useState } from "react";
import { useTranslation } from 'react-i18next';

import "./StoreRegistration.css"
import StoreOpeningTimesConfig from "../../storeConfig/components/StoreOpeningTimesConfig";

import 'react-time-picker/dist/TimePicker.css';

import BikeList from '../../bikeList/components/BikeList'
import PictureAndDescriptionField from "../../../components/IO/PictureAndDescriptionField";
import AddressField from "../../../components/IO/AddressField";

const StoreRegistration = () => {

    const { t } = useTranslation();

    return (
        <>
            <h1>{t('new_store')}</h1>
            <PictureAndDescriptionField editable={true}/>
            <AddressField editable={true}/>
            <StoreOpeningTimesConfig />

            <h2>{t('add_bikes_to_store')}</h2>
            <BikeList />

            <div className="button-container">
                <button type="button" className="button regular">{t('cancel')}</button>
                <button type="button" className="button accent">{t('register_new_store')}</button>
            </div>
        </>
    );
};

export default StoreRegistration;