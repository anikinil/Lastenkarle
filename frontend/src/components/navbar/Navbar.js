import React, { useContext, useEffect } from 'react';
import MenuItems from './MenuItems';
import './Navbar.css';
import logo from '../../assets/images/logo.png';
import { FaUser } from 'react-icons/fa';
import { ACCOUNT_DELETION, ALL_BIKES, ALL_BOOKINGS, ALL_STORES, ALL_USERS, BOOKING, BOOKINGS, ENROLLMENT, LOGIN, LOGOUT, MY_BOOKINGS, MY_STORES, REGIONAL_BOOKING, REGISTER, STORE_CONFIG, USERS } from '../../constants/URLs/Navigation';
import { REGION_NAME, STORE_NAME } from '../../constants/URLs/General';
import { Roles } from '../../constants/Roles';
import { useTranslation } from 'react-i18next';
import { AuthContext } from '../../AuthProvider';

const Navbar = () => {

    const { t } = useTranslation();

    const { userRoles, userStores } = useContext(AuthContext);

    // TODO make each title a translatoin constant
    // TODO use URL constants for each url
    const getMenuItems = () => {
        const storeItems = userStores.map((store) => ({ title: store, url: STORE_CONFIG.replace(STORE_NAME, store) }))
        const allItems = [
            {
                title: t('booking'),
                url: BOOKING,
                roles: [Roles.CUSTOMER, Roles.MANAGER, Roles.ADMINISTRATOR, Roles.VISITOR],
                submenu: [
                    {
                        title: 'Karlsruhe',
                        url: REGIONAL_BOOKING.replace(REGION_NAME, 'karlsruhe')
                    },
                    {
                        title: 'Ettlingen',
                        url: REGIONAL_BOOKING.replace(REGION_NAME, 'ettlingen')
                    },
                    {
                        title: 'Bruchsaal',
                        url: REGIONAL_BOOKING.replace(REGION_NAME, 'bruchsaal')
                    },
                    {
                        title: 'Malsch',
                        url: REGIONAL_BOOKING.replace(REGION_NAME, 'malsch')
                    }
                ]
            },
            {
                title: t('my_stores'),
                url: MY_STORES,
                roles: [Roles.MANAGER, Roles.ADMINISTRATOR],
                submenu: storeItems
            },
            {
                title: t('admin_activities'),
                roles: [Roles.ADMINISTRATOR],
                submenu: [
                    {
                        title: t('all_bookings'),
                        url: ALL_BOOKINGS,
                    },
                    {
                        title: t('all_users'),
                        url: ALL_USERS,
                    },
                    {
                        title: t('all_stores'),
                        url: ALL_STORES,
                    },
                    {
                        title: t('all_bikes'),
                        url: ALL_BIKES,
                    },
                    {
                        title: t('enrollment'),
                        url: ENROLLMENT,
                    }
                ]
            },
            {
                title: <FaUser />,
                url: MY_BOOKINGS,
                roles: [Roles.CUSTOMER, Roles.MANAGER, Roles.ADMINISTRATOR],
                submenu: [
                    {
                        title: t('logout'),
                        url: LOGOUT,
                    },
                    {
                        title: t('delete_account'),
                        url: ACCOUNT_DELETION,
                    }
                ]
            },
            {
                title: <FaUser />,
                url: null,
                roles: [Roles.VISITOR],
                submenu: [
                    {
                        title: t('login'),
                        url: LOGIN,
                    },
                    {
                        title: t('register'),
                        url: REGISTER,
                    }
                ]
            }
        ]

        return allItems.filter(item => userRoles.some(role => item.roles.includes(role)));
    };

    return (
        <div className='nav-area'>
            <a href='/' className='logo-container'>
                <img className='logo-img' src={logo} alt='Logo' />
            </a>
            <nav className='nav'>
                <ul className='menus'>
                    {getMenuItems(userStores).map((item, index) => (
                        <MenuItems key={index} item={item} />
                    ))}
                </ul>
            </nav>
        </div>
    );
}

export default Navbar;