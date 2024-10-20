import React from 'react';
import { useTranslation } from 'react-i18next';

// Function to get a cookie value by name
//Alma war hier TEST
const getCookie = (name) => {
    const cookies = document.cookie
        .split('; ')
        .find((row) => row.startsWith(`${name}=`));

    return cookies ? cookies.split('=')[1] : null;
};

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