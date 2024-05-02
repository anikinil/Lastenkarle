import React from 'react';
import { useState } from 'react';
import "./Navbar.css";

import MenuItem from './MenuItem';

const MenuItems = ({ item }) => {

    const userRoles = ['admin']; // TODO: make global, when fetching implemented

    return (
        <li>
            <MenuItem className="menu-item" item={item} userRoles={userRoles} />
        </li>
    );
};

export default MenuItems;