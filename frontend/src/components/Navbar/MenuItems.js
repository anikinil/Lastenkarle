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
                    <a className="menu-item" 
                        aria-haspopup="menu"
                        aria-expanded={dropdown ? "true" : "false"}
                        href={items.url}
                        style={items.url ? {cursor: "pointer"} : {cursor: "default"}}
                        >
                        {items.title}
                    </a>
                    <Dropdown submenus={items.submenu} dropdown={dropdown} />
                </>
            ) : (
                <a className='menu-item' href={items.url}>{items.title}</a>
            )}
        </li>
    );
};

export default MenuItems;