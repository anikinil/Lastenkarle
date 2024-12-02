import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { LOGIN, USER_DATA } from '../constants/URIs/UserURIs';
import { useNavigate } from 'react-router-dom';
import { HELMHOLTZ, HOME, REGISTER } from '../constants/URLs/Navigation';
import { getCookie, setCookie } from '../services/Cookies';
import { ERR_FETCHING_USER_DATA, ERR_POSTING_LOGIN_REQUEST } from '../constants/ErrorMessages';
import { Roles } from '../constants/Roles';

const Login = () => {
    // Translation hook
    const { t } = useTranslation();

    // Navigation hook
    const navigate = useNavigate();

    // State hooks for username and password
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    // Handle login button click
    function handleLoginClick() {
        postLogin();
    }

    // Post login request
    const postLogin = () => {
        let payload = {
            username: username,
            password: password
        };

        // Post login request
        fetch(LOGIN, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                if (response?.ok) {
                    return response.json();
                } else {
                    // If the request was not successful, throw an error
                    return response.json().then(errorData => {
                        throw new Error(errorData.message);
                    });
                }
            })
            // Set the token and user role state variables
            .then(data => {
                setCookie('token', data.token);
                fetchUserRoles();
                // TODO account for different locations from which user can log in and navigate back to them
                navigate(HOME);
            })
            .catch(error => {
                // Handle any network or other errors that occurred during the request
                alert(ERR_POSTING_LOGIN_REQUEST, error);
            });
    }

    const fetchUserRoles = () => {
        const token = getCookie('token');
        if (token !== 'undefined' && token !== null) {
            fetch(USER_DATA, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,
                }
            })
                .then(response => response.json())
                .then(data => {
                    // get the user flags from the response
                    const flags = data.user_flags.map(element => element.flag);
                    // get the store names from the flags
                    const stores = flags.filter(role => role.includes('Store: ')).map(role => role.replace('Store: ', ''));
                    // get the roles from the flags
                    const roles = (flags.filter(role => !role.includes('Store: ')));
                    // if the user is manager of at least one store, add the manager role
                    if (stores.length > 0) { roles.push(Roles.MANAGER); }
                    // set the cookies
                    setCookie('userRoles', roles);
                    setCookie('userStores', stores);
                })
                .catch(error => {
                    console.error(ERR_FETCHING_USER_DATA, error);
                });
        } else {
            setCookie('userRoles', [Roles.VISITOR]);
        }
    }

    // Handle Helmholtz login button click
    const handleHelmholtzLoginClick = () => {
        window.location.replace(HELMHOLTZ);
    }

    // Handle register button click
    const handleRegisterClick = () => {
        navigate(REGISTER);
    }

    // Prevent user from switching to a new line by hitting [Enter]
    const handleFieldKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    };

    return (
        <>
            {/* Login header */}
            <h1>{t('login')}</h1>

            {/* Username input field */}
            <textarea
                title={t('enter_username')}
                className='username'
                rows='1'
                value={username}
                onChange={e => setUsername(e.target.value)}
                onKeyDown={handleFieldKeyDown}
                placeholder={t('enter_username')}
            >
            </textarea>

            {/* Password input field */}
            <textarea
                title={t('enter_password')}
                className='password'
                rows='1'
                value={password}
                onChange={e => setPassword(e.target.value)}
                onKeyDown={handleFieldKeyDown}
                placeholder={t('enter_password')}
            >
            </textarea>

            {/* Button container */}
            <div className='button-container'>
                <button type='button' className='button accent' onClick={handleLoginClick}>{t('login')}</button>
                <button type='button' className='button regular' onClick={handleHelmholtzLoginClick}>{t('helmholtz_login')}</button>
                <button type='button' className='button regular' onClick={handleRegisterClick}>{t('register_instead')}</button>
            </div>
        </>
    );
};

export default Login;