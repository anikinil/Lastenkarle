import React from 'react';
import { useTranslation } from 'react-i18next';

const UserListItem = ({user}) => {

    const { t } = useTranslation();

    const handlePanelClick = () => {
        // TODO implement
        console.log(user.name)
    }

    const handleBookingsClick = e => {
        // TODO implement
        console.log('bookings')
        e.stopPropagation()
    }

    const handleBanClick = e => {
        // TODO implement
        console.log('ban')
        e.stopPropagation()
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