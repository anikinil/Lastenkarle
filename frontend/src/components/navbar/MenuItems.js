import React from 'react';
import './Navbar.css';

import MenuItem from './MenuItem';

// a list of menu items
const MenuItems = ({ item }) => {

    return (
        <li>
            <MenuItem className='menu-item' item={item} />
        </li>
    );
};

export default MenuItems;