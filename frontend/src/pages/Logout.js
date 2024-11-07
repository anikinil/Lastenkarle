import React, { useState, startTransition, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

import { LOGOUT } from '../constants/URIs/UserURIs';
import { useNavigate } from 'react-router-dom';
import { deleteCookie, getCookie } from '../services/Cookies';
import { LOGIN } from '../constants/URLs/Navigation';
import { ERR_POSTING_LOGOUT_REQUEST } from '../constants/ErrorMessages';

// This component handles the logout process
const Logout = () => {

    // Hook for translation
    const { t } = useTranslation();

    // State to store any error that occurs during logout
    const [error, setError] = useState(null);

    // Hook to navigate to different routes
    const navigate = useNavigate();

    // Retrieve the token from cookies
    const token = getCookie('token');

    // Function to handle the logout process
    function logout() {
        console.log("TOKEN LOGOUT", token);
        // Send the POST request to the server endpoint
        fetch(LOGOUT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
            .then(response => {
                console.log(token);
                if (response.ok) {
                    // If the response is successful, delete the token cookie
                    deleteCookie('token');
                    // Navigate to the login page
                    startTransition(() => {
                        navigate(LOGIN);
                    });
                } else {
                    // If the request was not successful, throw an error
                    return response.json().then(data => {
                        throw new Error(data.detail);
                    });
                }
            })
            .catch(error => {
                // Catch the error and set it in the state
                setError(error);
                console.log(ERR_POSTING_LOGOUT_REQUEST + ': ' + error);
            });
    }

    const handleLogoutClick = () => {
        logout();
    }

    const handleCancelClick = () => {
        navigate(-1);
    }   

    return (
        <>
            <h1>{t('are_you_sure_you_want_to_logout')}</h1>
            <div className='button-container'>
                <button type='button' className='button accent' onClick={handleLogoutClick}>{t('logout')}</button>
                <button type='button' className='button regular' onClick={handleCancelClick}>{t('cancel')}</button>
            </div>

        </>
    );
};

export default Logout;