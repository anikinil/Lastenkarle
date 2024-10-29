import React from 'react';
import { useTranslation } from 'react-i18next';
import { BAN_USER } from '../../../constants/URIs/AdminURIs';
import { useNavigate } from 'react-router-dom';

const UserListItem = ({user}) => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    const handlePanelClick = () => {
        navigate(`/user`, { state: {user: user }});
    }
    
    // navigates to booking list filtered by this user (so only bookings of this user are shown)
    const handleBookingsClick = e => {
        navigate(`/bookings`, { state: {user: user }});
        e.stopPropagation()
    }

    // bans the user
    const handleBanClick = e => {
        postBan();
        e.stopPropagation();
    }

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
        })
    }

    return (
        <li className='list-item' onClick={handlePanelClick}>

            <p className='list-item-label'>{user.name}</p>

            <button type='button' className='list-item-button regular' onClick={handleBookingsClick}>{t('bookings')}</button>
            <button type='button' className='list-item-button delete' onClick={handleBanClick}>{t('ban')}</button>
        </li>
    );
};
  
export default UserListItem;