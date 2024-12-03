import React, { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { getCookie } from '../services/Cookies';


const Home = () => {

    const token = getCookie('token'); 

    const { t } = useTranslation();

    return (
        <>
            <h1>{t('homepage')}</h1>
            <p>YOUR TOKEN: {token}</p>
        </>
    );
};

export default Home;