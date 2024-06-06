import React from "react";
import { useTranslation } from 'react-i18next';

const BikeRegistration = () => {

    const { t } = useTranslation();

    return (
        <>
            <h1>{t('new_bike')}</h1>
        </>
    );
};

export default BikeRegistration;