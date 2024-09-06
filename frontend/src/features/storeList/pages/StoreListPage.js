//Page of overview of all stores
//Shown to admin
import React from 'react';
import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css';

import StoreList from '../components/StoreList';

const StoreListPage = () => {

    const { t } = useTranslation();

    return (
        <>
            <h1>{t('stores')}</h1>

            <StoreList />
        </>
    );
};

export default StoreListPage;