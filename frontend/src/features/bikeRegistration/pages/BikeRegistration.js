import React, { useState } from "react";
import { useTranslation } from 'react-i18next';

import "./BikeRegistration.css"
import PictureAndDescriptionField from "../../../components/IO/PictureAndDescriptionField";

const BikeRegistration = () => {

    const { t } = useTranslation();

    return (
        <>
            <h1>{t('new_bike')}</h1>

            <PictureAndDescriptionField editable={true}/>

            {/* TODO add cancel button (to navigate to previous page) */}
            <div className="button-container">
                <button type="button" className="button register">{t('register_new_bike')}</button>
            </div>
        </>
    );
};

export default BikeRegistration;