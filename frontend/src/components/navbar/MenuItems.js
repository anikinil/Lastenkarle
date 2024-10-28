import React from 'react';
import './Navbar.css';

import MenuItem from './MenuItem';
import { getCookie } from '../../services/Cookies';

const MenuItems = ({ item }) => {

    const userRole = getCookie('user_role');

    return (
        <li>
            <MenuItem className='menu-item' item={item} userRole={userRole} />
        </li>
    );
};

export default MenuItems;