import React, { useEffect, useState } from 'react';
import { BAN_USER, SELECTED_USER } from '../../constants/URIs/AdminURIs';
import { ERR_FETCHING_USER_DATA } from '../../constants/ErrorMessages';
import { ID } from '../../constants/URIs/General';
import { useParams } from 'react-router-dom';
import { getCookie } from '../../services/Cookies';
import { useTranslation } from 'react-i18next';
import ConfirmationPopup from '../../components/confirmationDialog/ConfirmationPopup';


const UserPage = () => {

    const { t } = useTranslation(); // Translation hook

    const id = useParams().user; // Get bike ID from URL parameters

    const token = getCookie('token'); // Get authentication token from cookies

    const [user, setUser] = useState(); // State to store user data

    const fetchUser = () => {
        fetch(SELECTED_USER.replace(ID, id), {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
            .then(response => response.json())
            .then(data => {
                setUser(data); // Set user data to state
            })
            .catch(error => {
                console.error(ERR_FETCHING_USER_DATA, error); // Log error if fetching user fails
            });
    }

    // Function to send a POST request to ban the user
    const postBan = () => {
        let payload = {
            contact_data: user.contact_data
        };
        return fetch(BAN_USER, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify(payload)
        });
    }

    const handleBanClick = () => {
        // TODO confirmation dialog
        postBan();
    }

    useEffect(() => {
        fetchUser();
    }, []);

    return (
        <>
            {user &&
                <>
                    <h1>{user.username}</h1>
                    <h2>{t('contact_data')}</h2>
                    <p>{user.contact_data}</p>

                    <button onClick={handleBanClick}>Ban User</button>
                </>
            }
        </>
    );
}

export default UserPage;