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
        // Send the POST request to the server endpoint
        fetch(LOGOUT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
        .then(response => {
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

    // Hook to handle the logout process
    useEffect(() => {
        logout();
    }, []);
    
    return (
        <>
            {error ?
                // Display error message if there is an error
                <p>{t('logout_failed') + ': ' + error?.message}</p>
                :
                // Display logging out message if there is no error
                <p>{t('logging_out')}</p>
            }
        </>
    );
};

export default Logout;