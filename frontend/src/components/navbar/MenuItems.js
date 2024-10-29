import React from 'react';
import './Navbar.css';

import MenuItem from './MenuItem';

// a list of menu items
const MenuItems = ({ item, userRoles }) => {

    return (
        <li>
            <MenuItem className='menu-item' item={item} userRoles={userRoles} />
        </li>
    );
};

export default MenuItems;