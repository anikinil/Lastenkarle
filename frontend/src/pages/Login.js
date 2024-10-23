import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import { LOGIN as LOGIN_URI} from '../constants/URIs/UserURIs';
import { useNavigate } from 'react-router-dom';

const Login = () => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const [token, setToken] = useState()

    function handleLoginClick() {
        postLogin();
        setTokenCookie();
        navigateToNextPage();
    }

    // post login request
    const postLogin = () => {

        let payload = {
            username: username,
            password: password
        };

        // post login request
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
                    // if the request was not successful, throw an error
                    return response.json().then(errorData => {
                        throw new Error(errorData.message);
                    });
                }
            })
            // set the token variable to acquired token
            .then(data => {
                setToken(data.token);
            })
            .catch(error => {
                // handle any network or other errors that occurred during the request
                alert('Error making login request.' + error.message);
            });
    }

    const handleHelmholtzLoginClick = () => {
        // TODO use proper variable
        window.location.replace('URL_USER_HELMHOLTZ');
    }

    const handleRegisterClick = () => {
        // TODO account for different source and destination pages (maybe with cookies)
        navigate('/register')
    }

    const setTokenCookie = () => {
        var days = 1
        const expirationDate = new Date();
        expirationDate.setDate(expirationDate.getDate() + days);
        document.cookie = `${'token'}=${token}; expires=${expirationDate.toUTCString()}; path=/`;
    };

    // THINK if there is a good way to not have to add this funciton everywhere
    // this prevents user from switching to new line by hitting [Enter]
    // TODO perhaps use SingleLineTextFieldComponent
    const handleFieldKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    };

    const navigateToNextPage = () => {
        // TODO implement and account for different locations from which user can log in and navigate back to them
    }

    return (
        <>
            {/* THINK about style */}
            <h1>{t('login')}</h1>

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

            {/* TODO check if there is an extra textarea type for passwords */}
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

            <div className='button-container'>
                <button type='button' className='button accent' onClick={handleLoginClick}>{t('login')}</button>
                <button type='button' className='button regular' onClick={handleHelmholtzLoginClick}>{t('helmholtz_login')}</button>
                <button type='button' className='button regular' onClick={handleRegisterClick}>{t('register_instead')}</button>
            </div>
        </>
    );
};

export default Login;