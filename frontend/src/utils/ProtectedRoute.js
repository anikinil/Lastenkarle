// import React from 'react';
// import { Route, Redirect } from 'react-router-dom';

// export const ProtectedRoute = ({ component: Component, roles, userRoles, ...rest }) => {
//     const hasPermission = roles.every(role => userRoles.includes(role));

//     return (
//         <Route
//             {...rest}
//             render={(props) =>
//                 hasPermission ? <Component {...props} /> : <Redirect to="/error" />
//             }
//         />
//     );
// };

import React from 'react';
import { Route, Navigate } from 'react-router-dom';

export const ProtectedRoute = ({ element, roles, userRoles, ...rest }) => {

    const hasPermission = roles.every(role => userRoles.includes(role));

    // If the user is authenticated, render the provided element, otherwise redirect to the login page
    return hasPermission ? <Route {...rest} element={element} /> : <Navigate to="/no-permission" />;
}


