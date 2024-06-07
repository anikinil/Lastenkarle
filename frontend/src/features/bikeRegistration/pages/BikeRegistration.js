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
        </>
    );
};

export default BikeRegistration;