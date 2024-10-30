// Page of overview of all stores
// Shown to admin
import React from 'react';
import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css'; // Importing CSS for styling the list

import StoreList from '../components/StoreList'; // Importing the StoreList component

const StoreListPage = () => {
    const { t } = useTranslation(); // Hook for translation

    return (
        <>
            {/* Page title */}
            <h1>{t('stores')}</h1>

            {/* Component displaying the list of stores */}
            <StoreList />
        </>
    );
};

export default StoreListPage; // Exporting the component as default