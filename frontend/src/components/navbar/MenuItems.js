import React from 'react';
import Dropdown from './Dropdown';
import { useState } from 'react';
import "./Navbar.css";

const MenuItems = ({ items }) => {

    const userRoles = ['customer'];
    const hasPermission = (items) => { return userRoles.some(role => items.roles.includes(role)); }

    const [dropdown, setDropdown] = useState(false);

    return (
        <li className="menu-items"
            onMouseEnter={() => setDropdown(true)}
            onMouseLeave={() => setDropdown(false)}
        >
            { hasPermission(items) ? (

                items.submenu ? (
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
                )) : 
                null
            }
        </li>
    );
};

export default MenuItems;