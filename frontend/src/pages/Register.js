import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import { REGISTER, LOGIN } from '../constants/URIs/UserURIs';
import { useNavigate } from 'react-router-dom';

import { ERR_POSTING_REGISTER_REQUEST } from '../constants/ErrorMessages';

const Register = () => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    const [username, setUsername] = useState('');
    const [contactData, setContactData] = useState('');
    const [yearOfBirth, setYearOfBirth] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [password, setPassword] = useState('');

    const [token, setToken] = useState()

    const handleRegisterClick = () => {
        postRegister();
        setTokenCookie();
        navigateToNextPage();
    }

    const postRegister = () => {

        let payload = {
            contact_data: contactData,
            username: username,
            password: password,
        };

        if (yearOfBirth !== '') {
            payload.year_of_birth = yearOfBirth;
        }

        // Send the POST request to the server endpoint
        fetch(REGISTER, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
            // TODO check if async causing problems
            .then(async response => {
                if (response.ok) {
                    const text = await response.text();
                    if (!text.trim()) {
                        postLogin();
                    } else {
                        return JSON.parse(text);
                    }
                }
                else {
                    // If the request was not successful, throw an error
                    const errorData = await response.json();
                    throw new Error(errorData.message);
                }
            })
            .catch(error => {
                alert(ERR_POSTING_REGISTER_REQUEST + ' ' + error.message);
            });
    }

    // post login request after successful registration
    const postLogin = () => {

        let payload = {
            username: username,
            password: password
        };

        // post login request
        fetch(LOGIN, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        })
            // TODO check if async causing problems
            .then(async response => {
                if (response.ok) {
                    return response.json();
                } else {
                    // If the request was not successful, throw an error
                    const errorData = await response.json();
                    throw new Error(errorData.message);
                }
            })
            .then(data => {
                setToken(data.token);
            })
            .catch(error => {
                // TODO proper variable for error message
                // handles any network or other errors that occurred during the request
                alert('Error making login request: ' + error.message);
            });
    }

    const handleHelmholtzRegistrationClick = () => {
        // TODO proper variable for URL
        window.location.replace('URL_USER_HELMHOLTZ');
    }

    const setTokenCookie = () => {
        var days = 1
        const expirationDate = new Date();
        expirationDate.setDate(expirationDate.getDate() + days);
        document.cookie = `${'token'}=${token}; expires=${expirationDate.toUTCString()}; path=/`;
    };

    // this prevents user from switching to new line by hitting [Enter]
    const handleFieldKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    };

    const handleLoginClick = () => {
        // TODO proper variable for navigation
        // TODO account for different source and destination pages
        navigate('/login')
    }

    const navigateToNextPage = () => {
        navigate('/')
    }

    return (
        <>
            <h1>{t('register')}</h1>

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

            <textarea
                title={t('enter_contact_data')}
                className='contact-data'
                rows='1'
                value={contactData}
                onChange={e => setContactData(e.target.value)}
                onKeyDown={handleFieldKeyDown}
                placeholder={t('enter_contact_data')}
            >
            </textarea>

            <textarea
                title={t('enter_year_of_birth')}
                className='year-of-birth'
                rows='1'
                value={yearOfBirth}
                onChange={e => setYearOfBirth(e.target.value)}
                onKeyDown={handleFieldKeyDown}
                placeholder={t('enter_year_of_birth')}
            >
            </textarea>

            <textarea
                title={t('enter_first_name')}
                className='first_name'
                rows='1'
                value={firstName}
                onChange={e => setFirstName(e.target.value)}
                onKeyDown={handleFieldKeyDown}
                placeholder={t('enter_first_name')}
            >
            </textarea>

            <textarea
                title={t('enter_last_name')}
                className='last_name'
                rows='1'
                value={lastName}
                onChange={e => setLastName(e.target.value)}
                onKeyDown={handleFieldKeyDown}
                placeholder={t('enter_last_name')}
            >
            </textarea>

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
                <button type='button' className='button accent' onClick={handleRegisterClick}>{t('register')}</button>
                {/* TODO should be defined as "Register via Helmholtz AAI" in translation files */}
                <button type='button' className='button regular' onClick={handleHelmholtzRegistrationClick}>{t('helmholtz_registration')}</button>
                <button type='button' className='button regular' onClick={handleLoginClick}>{t('login_instead')}</button>
            </div>
        </>
    );
};

export default Register;