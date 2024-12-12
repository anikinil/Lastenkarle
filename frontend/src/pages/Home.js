import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { getCookie } from '../services/Cookies';
import { USER_DATA } from '../constants/URIs/UserURIs';


const Home = () => {

    const token = getCookie('token');

    const { t } = useTranslation();

    const [username, setUsername] = useState('');

    // TODO remove
    const fetchUserData = () => {
        fetch(USER_DATA, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
            .then(response => response.json())
            .then(data => {
                setUsername(data.username);
            })
            .catch(error => {
            });
    }

    useEffect(() => {
        fetchUserData();
    }, []);

    return (
        <>
            <h1>{t('homepage')}: {username}</h1>
            <p>YOUR TOKEN: {token}</p>
        </>
    );
};

export default Home;