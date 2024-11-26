import React, { useEffect, useState } from 'react';
import MenuItems from './MenuItems';
import './Navbar.css';
import logo from '../../assets/images/logo.png';
import { USER_DATA } from '../../constants/URIs/UserURIs';
import { getCookie } from '../../services/Cookies';
import { ERR_FETCHING_USER_FLAGS } from '../../constants/ErrorMessages';
import { useLocation } from 'react-router-dom';
import { FaUser } from 'react-icons/fa';
import { ACCOUNT_DELETION, ALL_BIKES, LOGIN, LOGOUT, REGIONAL_BOOKING, REGISTER, STORE_CONFIG } from '../../constants/URLs/Navigation';
import { REGION_NAME, STORE_NAME } from '../../constants/URLs/General';
import { Roles } from '../../constants/Roles';
import { useTranslation } from 'react-i18next';


const Navbar = () => {

    // TODO only update when necessairy

    const { t } = useTranslation();

    // gets the current location (Router) to update the navbar after cahnge of user roles
    const location = useLocation();

    const token = getCookie('token');

    // default role is visitor (not logged in)
    const [userRoles, setUserRoles] = useState([Roles.VISITOR]);
    const [userStores, setUserStores] = useState([]);
    const [filteredMenuItems, setFilteredMenuItems] = useState([]);

    // TODO make each title a translatoin constant
    // TODO use URL constants for each url
    const getMenuItems = (stores) => {
        const storeItems = stores.map((store) => ({ title: store, url: STORE_CONFIG.replace(STORE_NAME, store) }))
        const allItems = [
            {
                title: 'Booking',
                url: '/booking',
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
                url: '/my-stores',
                roles: [Roles.MANAGER, Roles.ADMINISTRATOR],
                submenu: storeItems
            },
            {
                title: t('admin_activities'),
                roles: [Roles.ADMINISTRATOR],
                submenu: [
                    {
                        title: t('bookings'),
                        url: '/bookings',
                    },
                    {
                        title: t('users'),
                        url: '/users',
                    },
                    {
                        title: t('all_stores'),
                        url: '/all-stores',
                    },
                    {
                        title: t('all_bikes'),
                        url: ALL_BIKES,
                    },
                    {
                        title: t('enrollment'),
                        url: '/enrollment',
                    }
                ]
            },
            {
                title: <FaUser />,
                url: '/my-bookings',
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

    // fetch user roles on first render, if token is present (user is logged in)
    useEffect(() => {
        const userRoles = getCookie('userRoles');
        if (userRoles) setUserRoles(userRoles.split(','));
        const userStores = getCookie('userStores');
        if (userStores) setUserStores(userStores.split(','));
    }, [location, t]);

    useEffect(() => {
        setFilteredMenuItems(getMenuItems(userStores));
    }, [userRoles]);

    return (
        <div className='nav-area'>
            <a href='/' className='logo-container'>
                <img className='logo-img' src={logo} alt='Logo' />
            </a>
            <nav className='nav'>
                <ul className='menus'>
                    {filteredMenuItems.length > 0 ? filteredMenuItems.map((item, index) => (
                        <MenuItems key={index} item={item} />
                    )) : null}
                </ul>
            </nav>
        </div>
    );
}

export default Navbar;