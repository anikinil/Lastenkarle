import React, { useContext, useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { useNavigate } from 'react-router-dom';
import { getCookie } from '../../../services/Cookies';
import { AuthContext } from '../../../AuthProvider';

import { Roles } from '../../../constants/Roles';
import StoreListItemAdmin from './listItemVersions/StoreListItemAdmin';
import StoreListItemManager from './listItemVersions/StoreListItemManager';

const StoreListItem = ({ store }) => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    // THINK maybe show big preview of bike image on clik on miniature preview (aplies to all versions)

    const token = getCookie('token');

    const { userRoles } = useContext(AuthContext);

    return (
        <>
            {userRoles.includes(Roles.ADMINISTRATOR) ?
                <StoreListItemAdmin store={store} key={store.name} /> :

                userRoles.includes(Roles.MANAGER) ?
                    <StoreListItemManager store={store} key={store.name} /> : null}

        </>
    );
};

export default StoreListItem;