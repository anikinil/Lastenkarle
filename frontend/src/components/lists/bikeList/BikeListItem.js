import React, { useContext, useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { useNavigate } from 'react-router-dom';
import { getCookie } from '../../../services/Cookies';
import { AuthContext } from '../../../AuthProvider';

import { Roles } from '../../../constants/Roles';
import BikeListItemAdmin from './bikeListItemVersions/BikeListItemAdmin';
import BikeListItemCustomer from './bikeListItemVersions/BikeListItemCustomer';
import BikeListItemManager from './bikeListItemVersions/BikeListItemManager';

const BikeListItem = ({ bike }) => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    // THINK maybe show big preview of bike image on clik on miniature preview (aplies to all versions)

    const token = getCookie('token');

    const { userRoles } = useContext(AuthContext);

    return (
        <>
            {userRoles.includes(Roles.ADMINISTRATOR) ?
                <BikeListItemAdmin bike={bike} key={bike.id} /> :

                userRoles.includes(Roles.MANAGER) ?
                    <BikeListItemManager bike={bike} key={bike.id} /> :
                    
                    <BikeListItemCustomer bike={bike} key={bike.id} />}
        </>
    );
};

export default BikeListItem;