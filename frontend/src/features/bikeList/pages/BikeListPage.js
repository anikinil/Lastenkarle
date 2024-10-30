import React from 'react';
import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css';
import BikeList from '../components/BikeList';
import '../components/BikeList.css'

// BikeListPage component definition
const BikeListPage = () => {

    // Hook for translation
    const { t } = useTranslation();

    return (
        <>
            {/* Page title */}
            <h1>{t('bikes')}</h1>

            {/* Bike list component */}
            <BikeList />
        </>
    );
};

// Export the BikeListPage component as default
export default BikeListPage;