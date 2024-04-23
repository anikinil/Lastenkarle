import React from 'react';
import Dropdown from './Dropdown';
import { useState } from 'react';
import "./Navbar.css";

const MenuItems = ({ items }) => {

    const [dropdown, setDropdown] = useState(false);

    return (
        <li className="menu-items"
            onMouseEnter={() => setDropdown(true)}
            onMouseLeave={() => setDropdown(false)}
        >
            {items.submenu ? (
                <>
                    <button type="button" 
                        aria-haspopup="menu"
                        aria-expanded={dropdown ? "true" : "false"}
                        >
                        {items.title}{' '}
                    </button>
                    <Dropdown submenus={items.submenu} dropdown={dropdown} />
                </>
            ) : (
                <a href={items.url}>{items.title}</a>
            )}
        </li>
    );
};

export default MenuItems;