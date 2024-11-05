import React from 'react';
import { menuItems, getAccountItemByRoles } from '../../data/menuData'
import MenuItems from './MenuItems';
import MenuItem from './MenuItem';
import './Navbar.css';
import logo from '../../assets/images/logo.png';

const Navbar = () => {

    // const userRoles = ['admin']; // TODO fetch
    const userRoles = ['visitor']

    const accountItem = getAccountItemByRoles(userRoles);

    console.log(accountItem)

    return (
            <div className='nav-area'>
                <a href='/' className='logo-container'>
                    <img className='logo-img' src={logo} alt='Logo'/>
                </a>
                <nav className='nav'>
                    <ul className='menus'>
                        {menuItems.map((item, index) => {
                            return <MenuItems item={item} key={index} userRoles={userRoles}/>;
                        })}
                        <li>
                            {console.log("userRoles (Navbar)", userRoles)}
                            <MenuItem className='account-menu-item' item={accountItem} userRoles={userRoles}/>
                        </li>
                    </ul>
                </nav>
            </div>
    );
}

export default Navbar;