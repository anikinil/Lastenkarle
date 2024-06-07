import React, { useState } from "react";
import { useTranslation } from 'react-i18next';

import "./BikeRegistration.css"

const BikeRegistration = () => {

    const { t } = useTranslation();

    const [pictureSelected, setPictureSelected] = useState(false);

    return (
        <>
            <h1>{t('new_bike')}</h1>

            <div className="new-bike-img-container">
                {pictureSelected ?
                    <img className="new-bike-img" alt={t('bike_image')} src="source"></img>
                    :
                    <p>{t('select_a_picture')}</p>
                }
            </div>

            <textarea title={t('bike_description')} className="new-bike-description"></textarea>

            <div className="button-container">
                <button type="button" className="button picture">{t('remove_picture')}</button>
                <button type="button" className="button register">{t('register_new_bike')}</button>
            </div>
        </>
    );
};

export default BikeRegistration;