import React, { createContext, useState, useEffect } from 'react';
import { getCookie } from './services/Cookies';
import { Roles } from './constants/Roles';

export const AuthContext = createContext();

// THINK maybe check if user owns a store and add "manager" to userRoles if so
// (needs to be adjusted everywhere where AuthProvider is used)
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
