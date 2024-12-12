import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';

import { AuthContext } from '../../../AuthProvider';

import { Roles } from '../../../constants/Roles';
import BikeListItemAdmin from './listItemVersions/BikeListItemAdmin';
import BikeListItemCustomer from './listItemVersions/BikeListItemCustomer';
import BikeListItemManager from './listItemVersions/BikeListItemManager';

const BikeListItem = ({ bike }) => {

    const { t } = useTranslation();

    // THINK maybe show big preview of bike image on clik on miniature preview (aplies to all versions)

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