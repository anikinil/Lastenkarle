import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import { useNavigate } from 'react-router-dom';

const BikeListItemManager = ({ bike }) => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    // TODO manager will have a seperate list of bikes in his own stores and all bikes in system

    return (
        <>
            <p>MANAGER</p>
        </>
    );
};

export default BikeListItemManager;