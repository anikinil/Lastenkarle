import React from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import { ACCOUNT_DELETION } from "../constants/URIs/UserURIs";
import { ERR_DELETING_ACCOUNT } from "../constants/ErrorMessages";
import { LOGIN } from "../constants/URLs/Navigation";
import { deleteCookie, getCookie } from "../services/Cookies";


const AccountDeletion = () => {

    const { t } = useTranslation(); // Translation hook
    const navigate = useNavigate(); // Navigation hook

    const token = getCookie('token');

    const postAccountDeletion = () => {
        // Send the DELETE request to the server endpoint
        fetch(ACCOUNT_DELETION, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
            .then(async response => {
                if (!response?.ok) {
                    // If the request was not successful, throw an error
                    const errorData = await response.json();
                    throw new Error(errorData.message);
                } else {
                    deleteCookie('token');
                }
            })
            .then(data => {
                // If the request was successful, navigate to the home page
                navigate(LOGIN);
            })
            .catch(error => {
                alert(ERR_DELETING_ACCOUNT + ' ' + error.message);
            });
    }

    const handleDeleteAccountClick = () => {
        postAccountDeletion();
    }

    const handleCancelClick = () => {
        navigate(-1);
    }

    return (
        <div>
            <h1>{t('account_deletion')}</h1>

            <p>{t('are_you_sure_you_want_to_delete_your_account')}</p>
            <div className='button-container'>
                <button className='button accent' onClick={handleDeleteAccountClick}>{t('delete_account')}</button>
                <button className='button regular' onClick={handleCancelClick}>{t('cancel')}</button>
            </div>
        </div>
    )
}

export default AccountDeletion;