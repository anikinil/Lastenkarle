import React, { useState } from "react";
import { useTranslation } from 'react-i18next';
import Switch from '../../../components/UI/Switch'

import "./StoreOpeningTimesConfig.css"

const StoreOpeningTimesConfig = () => {

    const { t } = useTranslation();



    return (
        <>
            <h2>{t('opening_times')}</h2>

            <Switch />
        </>
    );
};

export default StoreOpeningTimesConfig;