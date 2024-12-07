import React from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { BAN_USER } from '../../../../constants/URIs/AdminURIs';
import { getCookie } from '../../../../services/Cookies';

// Component to display a single user item in a list
const UserListItemAdmin = ({ user }) => {

    // Hook for translation
    const { t } = useTranslation();

    // Hook for navigation
    const navigate = useNavigate();

    // Retrieve token from cookies
    const token = getCookie('token');

    // Handle click on the user panel to navigate to user details
    const handlePanelClick = () => {
        navigate(`/user`, { state: { user: user } });
    }

    // Handle click on the bookings button to navigate to the user's bookings
    const handleBookingsClick = e => {
        navigate(`/bookings`, { state: { user: user } });
        e.stopPropagation(); // Prevent the click event from bubbling up to the panel
    }

    // Handle click on the ban button to ban the user
    const handleBanClick = e => {
        postBan(); // Call the function to ban the user
        e.stopPropagation(); // Prevent the click event from bubbling up to the panel
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

    return (
        <li className='list-item' onClick={handlePanelClick}>
            <p className='list-item-label'>{user.username? user.username : "(no username)"}</p>
            <button type='button' className='list-item-button regular' onClick={handleBookingsClick}>{t('bookings')}</button>
            <button type='button' className='list-item-button accent' onClick={handleBanClick}>{t('ban')}</button>
        </li>
    );
};

export default UserListItemAdmin;