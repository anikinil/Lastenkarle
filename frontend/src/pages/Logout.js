import React, { useState, startTransition } from 'react';
import { useTranslation } from 'react-i18next';

import { LOGOUT } from '../constants/URIs/UserURIs';
import { useNavigate } from 'react-router-dom';

// on successful logout this component does not show any content and only runs the logout script
// on failure it can display the error message to the user
const Logout = () => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    // TODO acquire token from cookie
    const [token, setToken] = useState('')
    const [error, setError] = useState()

    // logout call
    logout();

    // POST logout request
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
                        // TODO add proper variable for home navigation
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
                // TODO replace by proper variable
                console.log('Error making the logout request.');
                setError(error)
            });
    }

    // THINK if necessary
    const deleteTokenCookie = () => {
        // TODO implement
    };

    return (
        <>
            {error ?
                <span>{error?.message}</span>
                :
                null
            }
        </>
    );
};

export default Logout;