import React, { useContext, useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { AuthContext } from '../AuthProvider';
import { Roles } from '../constants/Roles';

// ProtectedElement component to restrict access based on user roles
export const ProtectedElement = ({element, elementRoles}) => {

    // Translation hook
    const { t } = useTranslation();

    const { userRoles, userStores } = useContext(AuthContext);
    const [hasPermission, setHasPermissoin] = useState(false)

    useEffect(() => {
        let roles = userRoles;
        if (userStores.length > 0) roles.push(Roles.MANAGER);
        setHasPermissoin(elementRoles.some(role => roles.includes(role)))
    }, [userRoles, userStores])

    // If the user has permission, render the provided element, otherwise redirect to the no-permission page
    return (hasPermission ? (
        element
    ) : (
        <h2>{t('you_have_no_permission_to_visit_page')}</h2>
    ));
}
