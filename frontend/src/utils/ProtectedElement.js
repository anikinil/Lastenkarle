import React from 'react';
import { Navigate } from 'react-router-dom';

export const ProtectedElement = ({element, elementRoles, userRoles}) => {

    const hasPermission = elementRoles.some(role => userRoles.includes(role));

    // If the user is authenticated, render the provided element, otherwise redirect to the no-permission page
    return (hasPermission ? (
        element
    ) : (
        <Navigate to='/no-permission' />
    ));
}


