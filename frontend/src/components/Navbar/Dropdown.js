import React from "react";
import "./Navbar.css";

const Dropdown = ({ submenus, dropdown }) => {
    return (
        <ul className={`dropdown ${dropdown ? "show" : "hide"}`}>
            {submenus.map((submenu, index) => (
                <li key={index} className="dropdown-items">
                    <a href={submenu.url}>{submenu.title}</a>
                </li>
            ))}
        </ul>
    );
};

export default Dropdown;