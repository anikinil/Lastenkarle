import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';


const Login = () => {

    const { t } = useTranslation();

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const [token, setToken] = useState()

    // function handleLoginClick() {
    //     postLogin();
    // }

    // POST login request
    // const postLogin = () => {

    //     let payload = {
    //         username: username,
    //         password: password
    //     };

    //     // POST login request
    //     fetch(URI_USER_LOGIN, {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body: JSON.stringify(payload)
    //     })
    //         .then(response => {
    //             if (response?.ok) {
    //                 return response.json();
    //             } else {
    //                 // If the request was not successful, throw an error
    //                 return response.json().then(errorData => {
    //                     throw new Error(errorData.message);
    //                 });
    //             }
    //         })
    //         .then(data => {
    //             const token = data.token;
    //             navigateToNextPage(token);
    //         })
    //         .catch(error => {
    //             // Handle any network or other errors that occurred during the request
    //             alert('Error making login request.' + error.message);
    //         });
    // }

    // const handeHelmholtzSignInClick = () => {
    //     window.location.replace(URL_USER_HELMHOLTZ);
    // }

    // const handleSignInClick = () => {
    //     // navigate to register page
    // }

    const setTokenCookie = () => {
        var days = 1
        const expirationDate = new Date();
        expirationDate.setDate(expirationDate.getDate() + days);
        document.cookie = `${'token'}=${token}; expires=${expirationDate.toUTCString()}; path=/`;
    };

    // this prevents user from switching to new line by hitting [Enter]
    const handleUsernameFieldKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    };

    return (
        <>
            <h1>{t('login')}</h1>

            <textarea
                title={t('enter_username')}
                className='username'
                rows='1'
                value={username}
                onChange={e => setUsername(e.target.value)}
                onKeyDown={handleUsernameFieldKeyDown}
                placeholder={t('enter_username')}
            >
            </textarea>

            <input type='text' value={username} onChange={e => setUsername(e.target.value)}></input>
            <button onClick={() => setTokenCookie()}>{t('submit')}</button>
        </>
    );
};

export default Login;