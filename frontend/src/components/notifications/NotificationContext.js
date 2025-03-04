import React, { createContext, useState, useContext } from 'react';
import NotificationOverlay from './NotificationOverlay';

const NotificationContext = createContext();

export const NotificationProvider = ({ children }) => {
    const [notification, setNotification] = useState(null);

    const showNotification = (message, type = 'info') => {
        setNotification({ message, type });
        setTimeout(() => {
            setNotification(null);
        }, 5000);
    };

    return (
        <NotificationContext.Provider value={{ showNotification }}>
            {children}
            {notification && <NotificationOverlay {...notification} />}
        </NotificationContext.Provider>
    );
};

export const useNotification = () => useContext(NotificationContext);
