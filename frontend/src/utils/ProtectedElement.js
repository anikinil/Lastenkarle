import React from 'react';
import { Navigate } from 'react-router-dom';

// ProtectedElement component to restrict access based on user roles
export const ProtectedElement = ({element, elementRoles, userRoles}) => {

    // Check if the user has at least one of the required roles
    const hasPermission = elementRoles.some(role => userRoles.includes(role));

    // If the user has permission, render the provided element, otherwise redirect to the no-permission page
    return (hasPermission ? (
        element
    ) : (
        <Navigate to='/no-permission' />
    ));
}
