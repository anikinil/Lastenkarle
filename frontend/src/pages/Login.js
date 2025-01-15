import React, { useCallback, useContext, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { LOGIN, USER_DATA } from '../constants/URIs/UserURIs';
import { useNavigate } from 'react-router-dom';
import { HELMHOLTZ, HOME, REGISTER } from '../constants/URLs/Navigation';
import { getCookie, setCookie } from '../services/Cookies';
import { ERR_FETCHING_USER_DATA, ERR_POSTING_LOGIN_REQUEST } from '../constants/ErrorMessages';
import { Roles } from '../constants/Roles';
import { AuthContext } from '../AuthProvider';

const Login = () => {
    const { t } = useTranslation();
    const { setUserRoles, setUserStores } = useContext(AuthContext);
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const postLogin = () => {
        const payload = { username, password };

        fetch(LOGIN, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        })
            .then(response => {
                if (response?.ok) return response.json();
                return response.json().then(errorData => {
                    throw new Error(errorData.message);
                });
            })
            .then(data => {
                setCookie('token', data.token);
                fetchUserRoles();
                navigate(HOME);
            })
            .catch(error => {
                alert(ERR_POSTING_LOGIN_REQUEST, error);
            });
    };

    const fetchUserRoles = () => {
        const token = getCookie('token');
        if (token !== 'undefined' && token !== null) {
            fetch(USER_DATA, {
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Token ${token}`,
                },
            })
                .then(response => response.json())
                .then(data => {
                    const flags = data.user_flags.map(element => element.flag);
                    const stores = flags.filter(role => role.includes('Store: ')).map(role => role.replace('Store: ', ''));
                    const roles = flags.filter(role => !role.includes('Store: '));
                    if (stores.length > 0) roles.push(Roles.MANAGER);
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
    };

    const handleHelmholtzLoginClick = () => {
        window.location.replace(HELMHOLTZ);
    };

    const handleRegisterClick = () => {
        navigate(REGISTER);
    };

    const handleSubmit = e => {
        e.preventDefault();
        postLogin();
    };

    return (
        <>
            <h1>{t('login')}</h1>
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
                    type='password'
                    title={t('enter_password')}
                    className='password'
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    placeholder={t('enter_password')}
                />
                <div className='button-container'>
                    <button type='submit' className='button accent'>{t('login')}</button>
                    <button type='button' className='button regular' onClick={handleHelmholtzLoginClick}>{t('helmholtz_login')}</button>
                    <button type='button' className='button regular' onClick={handleRegisterClick}>{t('register_instead')}</button>
                </div>
            </form>
        </>
    );
};

export default Login;
