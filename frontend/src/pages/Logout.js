import React, { useState, startTransition } from 'react';
import { useTranslation } from 'react-i18next';

import { LOGOUT } from '../constants/URIs/UserURIs';
import { useNavigate } from 'react-router-dom';
import { deleteCookie, getCookie } from '../services/Cookies';
import { LOGIN } from '../constants/URLs/Navigation';
import { ERR_POSTING_LOGOUT_REQUEST } from '../constants/ErrorMessages';

// on successful logout this component does not show any content and only runs the logout script 
// (maybe shows "Logging out..." message)
// on failure it can display the error message to the user
const Logout = () => {

    const { t } = useTranslation();

    const [error, setError] = useState(null);

    const navigate = useNavigate();

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
                    deleteCookie('token');
                    // TODO check if startTransition() needed
                    startTransition(() => {
                        navigate(LOGIN);
                    });
                } else {
                    // If the request was not successful throw an error
                    return response.json().then(data => {
                        throw new Error(data.detail);
                    });
                }
            })
            .catch(error => {
                // catch the error and print it to the console
                setError(error);
                console.log(ERR_POSTING_LOGOUT_REQUEST + ': ' + error);
            });
    }

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