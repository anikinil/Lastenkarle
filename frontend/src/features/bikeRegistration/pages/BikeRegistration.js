import React from "react";
import { useTranslation } from 'react-i18next';

import "./BikeRegistration.css"

const BikeRegistration = () => {

    const { t } = useTranslation();

    return (
        <>
            <h1>{t('new_bike')}</h1>

            <div className="new-bike-img-container">
                <img className="new-bike-img" alt={t('bike_image')} src="source"></img>
            </div>

            <textarea className="new-bike-description"></textarea>

            <div className="picture_buttons_container">
                <button type="button" className="button picture">{t('choose_picture')}</button>
                <button type="button" className="button picture">{t('remove_picture')}</button>
            </div>

            <button type="button" className="button register">{t('register_new_bike')}</button>
        </>
    );
};

export default BikeRegistration;