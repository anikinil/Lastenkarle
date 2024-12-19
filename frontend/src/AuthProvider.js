import React, { createContext, useState, useEffect } from 'react';
import { getCookie } from './services/Cookies';
import { Roles } from './constants/Roles';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {

    const [userRoles, setUserRoles] = useState([Roles.VISITOR]);
    const [userStores, setUserStores] = useState([]);

    const updateUserData = () => {
        const userRoles = getCookie('userRoles');
        if (userRoles) setUserRoles(userRoles.split(','));
        const userStores = getCookie('userStores');
        if (userStores) setUserStores(userStores.split(','));
    }

    useEffect(() => {
        
        updateUserData();
        window.addEventListener('cookieChange', updateUserData);
        return () => {
            window.removeEventListener('cookieChange', updateUserData);
        };
    }, []);

    return (
        <AuthContext.Provider value={{ userRoles, setUserRoles, userStores, setUserStores}}>
            {children}
        </AuthContext.Provider>
    );
};
