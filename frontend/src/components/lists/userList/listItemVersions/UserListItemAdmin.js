import React from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { getCookie } from '../../../../services/Cookies';
import { USER_PAGE } from '../../../../constants/URLs/Navigation';
import { ID } from '../../../../constants/URLs/General';

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
        navigate(USER_PAGE.replace(ID, user.id));
    }

    // Handle click on the bookings button to navigate to the user's bookings
    const handleBookingsClick = e => {
        navigate(`/bookings`, { state: { user: user } });
        e.stopPropagation(); // Prevent the click event from bubbling up to the panel
    }

    return (
        <li className='list-item' onClick={handlePanelClick}>
            <p className='list-item-label'>{user.username? user.username : "(no username)"}</p>
            <button type='button' className='list-item-button regular' onClick={handleBookingsClick}>{t('bookings')}</button>
        </li>
    );
};

export default UserListItemAdmin;