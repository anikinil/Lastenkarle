import React from 'react';
import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css';

import StoreList from '../components/StoreList';

// TODO seperate list comp from page, adjust navigation


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