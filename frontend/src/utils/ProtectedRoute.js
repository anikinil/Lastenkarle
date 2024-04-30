import React from 'react';
import { Route, Navigate } from 'react-router-dom';

export const ProtectedRoute = ({ element, routeRoles, userRoles, ...rest }) => {

    const hasPermission = routeRoles.some(role => userRoles.includes(role));

    // If the user is authenticated, render the provided element, otherwise redirect to the no-permission page
    return hasPermission ? <Route {...rest} element={element} /> : <Navigate to="/no-permission" />;
}


