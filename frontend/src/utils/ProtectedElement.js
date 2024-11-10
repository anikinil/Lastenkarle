import React, { useEffect, useState } from 'react';
import { getCookie } from '../services/Cookies';
import { USER_DATA } from '../constants/URIs/UserURIs';
import { ERR_FETCHING_USER_FLAGS } from '../constants/ErrorMessages';
import { useTranslation } from 'react-i18next';

// ProtectedElement component to restrict access based on user roles
export const ProtectedElement = ({element, elementRoles}) => {

    // Translation hook
    const { t } = useTranslation();

    const [hasPermission, setHasPermissoin] = useState(false)

    const fetchUserRoles = () => {
        const token = getCookie('token');
        console.log('TOKEN', token)
        if (token !== 'undefined' && token !== null) {
            console.log("TOKEN FOUND")
            fetch(USER_DATA, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,
                }
            })
                .then(response => response.json())
                .then(data => {
                    const userRoles = data.user_flags.map(element => element.flag)
                    setHasPermissoin(elementRoles.some(role => userRoles.includes(role)))
                })
                .catch(error => {
                    console.error(ERR_FETCHING_USER_FLAGS, error);
                });
        } else {
            // setUserRoles([Roles.VISITOR]);
            setHasPermissoin(false)
        }
    }

    useEffect(() => {
        fetchUserRoles();
    }, [])

    // If the user has permission, render the provided element, otherwise redirect to the no-permission page
    return (hasPermission ? (
        element
    ) : (
        <h2>{t('you_have_no_permission_to_visit_page')}</h2>
    ));
}
