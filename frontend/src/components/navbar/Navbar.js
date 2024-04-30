import React from "react";
// import "./Navbar.css";
import { menuData } from "../../data/menuData"
import MenuItems from "./MenuItems";
import "./Navbar.css";
import logo from "../../assets/images/logo.png";

const Navbar = () => {

    return (
        <header>
            <div className="nav-area">
                <a href="/" className="logo">
                    <img className="logo-img" src={logo} alt="Logo"/>
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