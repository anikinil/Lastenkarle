import React from 'react';
import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css';
import BikeList from '../components/BikeList';
import '../components/BikeList.css'

const BikeListPage = () => {

    const { t } = useTranslation();

    return (
        <>
            <h1>{t('bikes')}</h1>

            <BikeList />
        </>
    );
};

export default BikeListPage;