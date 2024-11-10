import React, { useEffect, useState } from 'react';
import { menuItems, Roles } from '../../components/navbar/menuData'
import MenuItems from './MenuItems';
import './Navbar.css';
import logo from '../../assets/images/logo.png';
import { USER_DATA } from '../../constants/URIs/UserURIs';
import { getCookie } from '../../services/Cookies';
import { ERR_FETCHING_USER_FLAGS } from '../../constants/ErrorMessages';
import { useLocation } from 'react-router-dom';

const Navbar = () => {

    // gets the current location (Router) to update the navbar after cahnge of user roles
    const location = useLocation();

    const token = getCookie('token');

    // default role is visitor (not logged in)
    const [userRoles, setUserRoles] = useState([Roles.VISITOR]);
    const [filteredMenuItems, setFilteredMenuItems] = useState([]);
    
    const fetchUserRoles = () => {
        if (token !== 'undefined' && token !== null) {
            fetch(USER_DATA, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,
                }
            })
            .then(response => response.json())
            .then(data => {
                setUserRoles(data.user_flags.map(element => element.flag));
            })
            .catch(error => {
                console.error(ERR_FETCHING_USER_FLAGS, error);
            });
        } else {
            setUserRoles([Roles.VISITOR]);
        }
    }

    // fetch user roles on first render, if token is present (user is logged in)
    useEffect(() => {
        fetchUserRoles();
    }, [location]);

    useEffect(() => {
        let filteredItems = menuItems.filter(item =>
            userRoles.some(role => item.roles.includes(role))
        );
        setFilteredMenuItems(filteredItems);
    }, [userRoles]);

    return (
        <div className='nav-area'>
            <a href='/' className='logo-container'>
                <img className='logo-img' src={logo} alt='Logo' />
            </a>
            <nav className='nav'>
                <ul className='menus'>
                    {filteredMenuItems.length > 0 ? filteredMenuItems.map((item, index) => (
                        <MenuItems key={index} item={item} />
                    )) : null}
                </ul>
            </nav>
        </div>
    );
}

export default Navbar;