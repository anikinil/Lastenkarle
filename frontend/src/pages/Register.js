import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import { REGISTER, LOGIN } from '../constants/URIs/UserURIs';

const Register = () => {

    const { t } = useTranslation();

    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [password, setPassword] = useState('');

    const [token, setToken] = useState()

    const handleSubmitClick = () => {
        postRegister();
        setTokenCookie();
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
            .then(response => {
                if (response.ok) {
                    return response.text().then(text => {
                        if (!text.trim()) {
                            postLogin();
                        } else {
                            return JSON.parse(text);
                        }
                    });

                }
                else {
                    // If the request was not successful, throw an error
                    return response.json().then(errorData => {
                        throw new Error(errorData.message);
                    });
                }
            })
            .catch(error => {
                // TODO add error message constants
                // Handle any network or other errors that occurred during the request
                alert(ERR_MAKING_REGISTER_REQUEST + ' ' + error.message);
            });
    }

    // POST login request after successful registration
    const postLogin = () => {

        let payload = {
            username: username,
            password: password
        };

        // POST login request
        fetch(LOGIN, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    // If the request was not successful, throw an error
                    return response.json().then(errorData => {
                        throw new Error(errorData.message);
                    });
                }
            })
            .then(data => {
                setToken(data.token);
                navigateToNextPage();
            })
            .catch(error => {
                // TODO remove magic number
                // Handle any network or other errors that occurred during the request
                alert('Error making login request: ' + error.message);
            });
    }

    const handleHelmholtzRegistrationClick = () => {
        window.location.replace(URL_USER_HELMHOLTZ);
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

    const navigateToNextPage = () => {
        // TODO implement
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
                title={t('enter_email')}
                className='email'
                rows='1'
                value={email}
                onChange={e => setEmail(e.target.value)}
                onKeyDown={handleFieldKeyDown}
                placeholder={t('enter_email')}
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

            <input type='text' value={username} onChange={e => setUsername(e.target.value)}></input>
            <button onClick={handleSubmitClick}>{t('submit')}</button>

            {/* TODO should be defined as "Register via Helmholtz AAI" in translation files */}
            <button onClick={handleHelmholtzRegistrationClick}>{t('helmholtz_registration')}</button>
        </>
    );
};

export default Register;