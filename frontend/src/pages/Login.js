import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { LOGIN as LOGIN_URI, REGISTER } from '../constants/URIs/UserURIs';
import { useNavigate } from 'react-router-dom';
import { HELMHOLTZ, HOME } from '../constants/URLs/Navigation';

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
        fetch(LOGIN_URI, {
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
                // TODO account for different locations from which user can log in and navigate back to them
                navigate(HOME);
                console.log("TOKEN", data.token);
            })
            .catch(error => {
                // Handle any network or other errors that occurred during the request
                alert('Error making login request.' + error.message);
            });
    }

    // Handle Helmholtz login button click
    const handleHelmholtzLoginClick = () => {
        window.location.replace(HELMHOLTZ);
    }

    // Handle register button click
    const handleRegisterClick = () => {
        navigate(REGISTER);
    }

    // Set a cookie with a specified label and value
    const setCookie = (label, value) => {
        var days = 1;
        const expirationDate = new Date();
        expirationDate.setDate(expirationDate.getDate() + days);
        document.cookie = `${label}=${value}; expires=${expirationDate.toUTCString()}; path=/`;
    };

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