import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { getCookie } from '../services/Cookies';
import { USER_DATA } from '../constants/URIs/UserURIs';
import Renting from '../features/renting/pages/Renting';


const Home = () => {

    const token = getCookie('token');

    const { t } = useTranslation();

    const [username, setUsername] = useState('');

    // TODO remove, when not needed
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
            {/* developement purposes */}
            <div align='left'>
                <p>Username: {username}</p>
                <p>Token: {token}</p>
            </div>

            <Renting />
        </>
    );
};

export default Home;