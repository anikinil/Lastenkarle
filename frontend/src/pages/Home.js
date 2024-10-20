import React from 'react';
import { useTranslation } from 'react-i18next';
import { getCookie } from '../services/Cookies';

// Example: Get the value of the 'username' cookie
const username = getCookie('username');

const Home = () => {

    const { t } = useTranslation();

    return (
        <>
            <h1>{t('homepage')}</h1>
            <p>You are {username ? username : 'unknown'}.</p>
        </>
    );
};

export default Home;