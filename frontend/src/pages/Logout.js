import React, { useState, startTransition } from 'react';
import { useTranslation } from 'react-i18next';

import { LOGOUT } from '../constants/URIs/UserURIs';
import { useNavigate } from 'react-router-dom';
import { getCookie } from '../services/Cookies';

// on successful logout this component does not show any content and only runs the logout script 
// (maybe shows "Logging out..." message)
// on failure it can display the error message to the user
const Logout = () => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    // TODO acquire token from cookie
    const [error, setError] = useState()

    const token = getCookie('token')

    // logout call
    logout();

    // post logout request
    function logout() {
        // Send the POST request to the server endpoint
        fetch(LOGOUT, {
            method: 'POST',
            headers: {
                'Authorization': `Token ${token}`
            }
        })
            .then(response => {
                if (response.ok) {
                    // TODO check if startTransition() needed
                    startTransition(() => {
                        // TODO add proper variable for navigation
                        navigate('/');
                    });
                } else {
                    // If the request was not successful throw an error
                    return response.json().then(data => {
                        throw new Error(data.detail);
                    });
                }
            })
            .catch(error => {
                // TODO add proper variable for error message
                console.log('Error making the logout request.');
                setError(error)
            });
    }

    // THINK if necessary
    const deleteTokenCookie = () => {

    };

    return (
        <>
            {error ?
                <p>{t('logout_failed') + ': ' + error?.message}</p>
                :
                <p>{t('logging_out')}</p>
            }
        </>
    );
};

export default Logout;