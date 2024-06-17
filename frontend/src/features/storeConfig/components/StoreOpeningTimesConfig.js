import React, { useState } from "react";
import { useTranslation } from 'react-i18next';
import Switch from '../../../components/UI/Switch'

import "./StoreOpeningTimesConfig.css"

const StoreOpeningTimesConfig = () => {

    const { t } = useTranslation();

    const [mondayOpen, setMondayOpen] = useState(false);

    return (
        <>
            <h2>{t('opening_times')}</h2>

            <p>Monday</p>
            <Switch isOn={mondayOpen} handleToggle={() => setMondayOpen(!mondayOpen)}/>
        </>
    );
};

export default StoreOpeningTimesConfig;