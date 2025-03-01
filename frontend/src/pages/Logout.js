import React, { useEffect } from 'react';
import { useTranslation } from 'react-i18next';

import { LOGOUT } from '../constants/URIs/UserURIs';
import { useNavigate } from 'react-router-dom';
import { deleteCookie, getCookie } from '../services/Cookies';
import { LOGIN } from '../constants/URLs/Navigation';
import { ERR_POSTING_LOGOUT_REQUEST } from '../constants/ErrorMessages';
import { AuthContext } from '../AuthProvider';
import { useContext } from 'react';
import { Roles } from '../constants/Roles';

// This component handles the logout process
const Logout = () => {

    const { setUserRoles, setUserStores } = useContext(AuthContext);

    // Hook for translation
    const { t } = useTranslation();

    // Hook to navigate to different routes
    const navigate = useNavigate();

    // JAN for some reason returns error "user is not authorized" when trying to logout, but user still gets logged out
    // Function to handle the logout process
    function logout(token) {
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
                    deleteCookie('userRoles');
                    deleteCookie('userStores');
                    setUserRoles([Roles.VISITOR]);
                    setUserStores([]);
                    // Navigate to the login page
                    navigate(LOGIN);
                } else {
                    // If the request was not successful, throw an error
                    return response.json().then(data => {
                        throw new Error(data.detail);
                    });
                }
            })
            .catch(error => {
                // Handle any network or other errors that occurred during the request
                console.log(ERR_POSTING_LOGOUT_REQUEST + ': ' + error);
            });
    }

    useEffect(() => {
        logout(getCookie('token'));
    }, []);

    return (
        <>
            <h1>{t('logging_out')}</h1>
        </>
    );
};

export default Logout;