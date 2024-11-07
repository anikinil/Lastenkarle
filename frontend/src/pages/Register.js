import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { LOGIN as LOGIN_URI, REGISTER } from '../constants/URIs/UserURIs';
import { useNavigate } from 'react-router-dom';
import { HELMHOLTZ, HOME, LOGIN as LOGIN_URL } from '../constants/URLs/Navigation';
import { ERR_POSTING_LOGIN_REQUEST, ERR_POSTING_REGISTER_REQUEST } from '../constants/ErrorMessages';

const Register = () => {
    const { t } = useTranslation(); // Translation hook
    const navigate = useNavigate(); // Navigation hook

    // State variables for form fields
    const [username, setUsername] = useState('');
    const [contactData, setContactData] = useState('');
    const [yearOfBirth, setYearOfBirth] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [password, setPassword] = useState('');

    // Handle register button click
    const handleRegisterClick = () => {
        postRegister();
        postLogin();
    };

    // Function to post registration data
    const postRegister = () => {

        let payload = {
            contact_data: contactData,
            username: username,
            password: password
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
            // TODO add navigation and account for different locations where user needs to be navigated to
            .then(async response => {
                if (!response?.ok) {
                    // If the request was not successful, throw an error
                    const errorData = await response.json();
                    throw new Error(errorData.message);
                }
            })
            .catch(error => {
                alert(ERR_POSTING_REGISTER_REQUEST + ' ' + error.message);
            });
    };

    // TODO think about how to avoid duplicate code (Login.js)
    // Function to post login data after successful registration
    const postLogin = () => {
        let payload = {
            username: username,
            password: password
        };

        // Send the POST request to the login endpoint
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
            }).then(data => {
                setTokenCookie(data.token);
                navigate(HOME);
            })
            .catch(error => {
                alert(ERR_POSTING_LOGIN_REQUEST + ' ' + error.message);
            });
    };

    // Handle Helmholtz registration button click
    const handleHelmholtzRegistrationClick = () => {
        window.location.replace(HELMHOLTZ);
    };

    // Function to set token cookie
    const setTokenCookie = (token) => {
        var days = 1;
        const expirationDate = new Date();
        expirationDate.setDate(expirationDate.getDate() + days);
        document.cookie = `${'token'}=${token}; expires=${expirationDate.toUTCString()}; path=/`;
    };

    // Prevent user from switching to new line by hitting [Enter]
    const handleFieldKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    };

    // Handle login button click
    const handleLoginClick = () => {
        navigate(LOGIN_URL);
    };

    // TODO use SingleLineInput component everywhere
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
                <button type='button' className='button regular' onClick={handleHelmholtzRegistrationClick}>{t('helmholtz_registration')}</button>
                <button type='button' className='button regular' onClick={handleLoginClick}>{t('login_instead')}</button>
            </div>
        </>
    );
};

export default Register;
