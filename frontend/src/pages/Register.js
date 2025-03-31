import React, { useContext, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { LOGIN as LOGIN_URI, REGISTER, USER_DATA } from '../constants/URIs/UserURIs';
import { useNavigate } from 'react-router-dom';
import { HELMHOLTZ, HOME, LOGIN as LOGIN_URL } from '../constants/URLs/Navigation';
import { ERR_FETCHING_USER_DATA, ERR_POSTING_LOGIN_REQUEST, ERR_POSTING_REGISTER_REQUEST } from '../constants/messages/ErrorMessages';
import { AuthContext } from '../AuthProvider';
import { getCookie, setCookie } from '../services/Cookies';
import { Roles } from '../constants/Roles';

import { useNotification } from '../components/notifications/NotificationContext';

const Register = () => {
    const { t } = useTranslation(); // Translation hook
    const navigate = useNavigate(); // Navigation hook

    const { showNotification } = useNotification(); // Notification hook

    const { setUserRoles, setUserStores } = useContext(AuthContext);

    // State variables for form fields
    const [username, setUsername] = useState('');
    const [contactData, setContactData] = useState('');
    const [yearOfBirth, setYearOfBirth] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [password, setPassword] = useState('');

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
                if (response?.ok) {
                    postLogin();
                } else {
                    // If the request was not successful, throw an error
                    const errorData = await response.json();
                    throw new Error(errorData.message);
                }
            })
            .catch(error => {
                showNotification(`${ERR_POSTING_REGISTER_REQUEST} ${error.message}`, 'error');
            });
    };

    // THINK about how to avoid duplicate code (Login.js)
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
            })
            .then(data => {
                setCookie('token', data.token);
                fetchUserRoles();
                // TODO account for different locations from which user can log in and navigate back to them
                navigate(HOME);
            })
            .catch(error => {
                showNotification(`${ERR_POSTING_LOGIN_REQUEST} ${error.message}`);
            });
    };


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
                    setUserRoles(roles);
                    setUserStores(stores);
                })
                .catch(error => {
                    console.error(ERR_FETCHING_USER_DATA, error);
                });
        } else {
            setCookie('userRoles', [Roles.VISITOR]);
        }
    }

    // Handle Helmholtz registration button click
    const handleHelmholtzRegistrationClick = () => {
        window.location.replace(HELMHOLTZ);
    }

    // // Prevent user from switching to new line by hitting [Enter]
    // const handleFieldKeyDown = (event) => {
    //     if (event.key === 'Enter') {
    //         event.preventDefault();
    //     }
    // };

    // Handle login button click
    const handleLoginClick = () => {
        navigate(LOGIN_URL);
    };

    const handleSubmit = e => {
        e.preventDefault();
        postRegister();
    };

    return (
        <>
            <h1>{t('register')}</h1>

            <form onSubmit={handleSubmit}>

                <input
                    type='text'
                    title={t('enter_username')}
                    className='username'
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                    placeholder={t('enter_username')}
                />

                <input
                    type='text'
                    title={t('enter_contact_data')}
                    className='contact-data'
                    value={contactData}
                    onChange={e => setContactData(e.target.value)}
                    placeholder={t('enter_contact_data')}
                />

                <input
                    type='number'
                    title={t('enter_year_of_birth')}
                    className='year-of-birth'
                    value={yearOfBirth}
                    onChange={e => setYearOfBirth(e.target.value)}
                    placeholder={t('enter_year_of_birth')}
                />

                <input
                    type='text'
                    title={t('enter_first_name')}
                    className='first-name'
                    value={firstName}
                    onChange={e => setFirstName(e.target.value)}
                    placeholder={t('enter_first_name')}
                />

                <input
                    type='text'
                    title={t('enter_last_name')}
                    className='last-name'
                    value={lastName}
                    onChange={e => setLastName(e.target.value)}
                    placeholder={t('enter_last_name')}
                />

                <input
                    type='password'
                    title={t('enter_password')}
                    className='password'
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    placeholder={t('enter_password')}
                />

                <div className='button-container'>
                    <button type='submit' className='button accent'>{t('register')}</button>
                    <button type='button' className='button regular' onClick={handleHelmholtzRegistrationClick}>{t('helmholtz_registration')}</button>
                    <button type='button' className='button regular' onClick={handleLoginClick}>{t('login_instead')}</button>
                </div>
            </form>
        </>
    );
};

export default Register;
