import React from 'react';
import './Navbar.css';

import MenuItem from './MenuItem';
import { getCookie } from '../../services/Cookies';

const MenuItems = ({ item }) => {

    const userRoles = getCookie('user_roles');

    return (
        <li>
            <MenuItem className='menu-item' item={item} userRoles={userRoles} />
        </li>
    );
};

export default MenuItems;