import React, { useState } from "react";
import { useTranslation } from 'react-i18next';

import "./BikeRegistration.css"
import PictureAndDescriptionEdit from "../../../components/dataEditing/PictureAndDescriptionEdit";

const BikeRegistration = () => {

    const { t } = useTranslation();

    return (
        <>
            <h1>{t('new_bike')}</h1>

            <PictureAndDescriptionEdit />

            <div className="button-container">
                <button type="button" className="button register">{t('register_new_bike')}</button>
            </div>
        </>
    );
};

export default BikeRegistration;