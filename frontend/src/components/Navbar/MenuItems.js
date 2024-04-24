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
                    <div className="link" 
                        aria-haspopup="menu"
                        aria-expanded={dropdown ? "true" : "false"}
                        >
                        <a href={items.url}>{items.title}</a>
                    </div>
                    <Dropdown submenus={items.submenu} dropdown={dropdown} />
                </>
            ) : (
                <div className='link'>
                    <a href={items.url}>{items.title}</a>
                </div>
            )}
        </li>
    );
};

export default MenuItems;