import React from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import StoreList from '../features/storeList/pages/StoreList';

export const ProtectedElement = ({element, elementRoles, userRoles}) => {

    console.log(element)

    const hasPermission = elementRoles.some(role => userRoles.includes(role));

    // If the user is authenticated, render the provided element, otherwise redirect to the no-permission page
    return (hasPermission ? (
        element
    ) : (
        <Navigate to="/no-permission" />
    ));
}


