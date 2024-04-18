import React from "react";
// import "./Navbar.css";
import { menuData } from "../../data/menuData"
import MenuItems from "./MenuItems";
import "./Navbar.css";


const Navbar = () => {
    return (
        <header>
            <div className="nav-area">
                <a href="/" className="logo">
                    Logo
                </a>
                <nav className="nav">
                    <ul className="menus">
                        {menuData.map((menu, index) => {
                            return <MenuItems items={menu} key={index} />;
                        })}
                    </ul>
                </nav>
            </div>
        </header>
    );
}

export default Navbar;