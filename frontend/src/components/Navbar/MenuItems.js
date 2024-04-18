import React from 'react';
import Dropdown from './Dropdown';
import { useState } from 'react';
import "./Navbar.css";

const MenuItems = ({ items }) => {

    const [dropdown, setDropdown] = useState(false);

    return (
        <li className="menu-items">
            {items.submenu ? (
                <>
                    <button type="button" 
                        aria-haspopup="menu"
                        aria-expanded={dropdown ? "true" : "false"}
                        onClick={() => setDropdown((prev) => !prev)}
                        >
                        {items.title}{' '}
                    </button>
                    {console.log(items.submenu)}
                    <Dropdown submenus={items.submenu} dropdown={dropdown} />
                </>
            ) : (
                <a href={items.url}>{items.title}</a>
            )}
        </li>
    );
};

export default MenuItems;