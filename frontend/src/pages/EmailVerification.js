import React, {useEffect, useState} from 'react';

import { useTranslation } from 'react-i18next';
import {useNavigate, useParams} from "react-router-dom";
import { ID, KEY } from '../constants/URIs/General';
import { HOME } from '../constants/URLs/Navigation';
import { EMAIL_VERIFICATION } from '../constants/URIs/UserURIs';
import { ERR_POSTING_EMAIL_VERIFICATION } from '../constants/ErrorMessages';


const EmailVerification = () => {

    const { t } = useTranslation('');

    const navigate = useNavigate();

    const params = useParams();
    const id = params.id;
    const key = params.key;

    const [verificationSuccessful, setVerificationSuccessful] = useState(false);

    // Function to send the POST request to the server
    const postVerification = () => {
        fetch(EMAIL_VERIFICATION.replace(ID, id).replace(KEY, key), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(response => {
                if (response?.ok) {
                    setVerificationSuccessful(true)
                    return response.json();
                }
                else {
                    // If the request was not successful, throw an error
                    return response.json().then(error => {
                        throw new Error(error.message);
                    });
                }
            })
            .catch(error => {
                alert(ERR_POSTING_EMAIL_VERIFICATION + error.message)
            })
    }

    // useEffect(() => {
    //     postVerification()
    // }, []);

    const handleOkClick = () => {
        navigate(HOME);    
    }

    return (
        <>
            <h1>{t('heading')}</h1>

            <div className='button-container'>
                <button className='button accent' onClick={postVerification}>{t('verify_email')}</button>
            </div>

            { verificationSuccessful ?
                <>
                    <h2>{t('email_verification_successful')}</h2>
                    <div className='button-container'>
                        <button className='button accent' onClick={handleOkClick}>{t('continue')}</button>
                    </div>
                </>
                :
                <>
                    <h2>{t('something_went_wrong')}</h2>
                </>
            }
        </>
    );
}

export default EmailVerification;