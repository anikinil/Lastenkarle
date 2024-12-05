import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import { useNavigate } from 'react-router-dom';

const BikeListItemManager = ({ bike }) => {

    const { t } = useTranslation();

    const navigate = useNavigate();

   
    return (
        <>
            <p>MANAGER</p>
        </>
    );
};

export default BikeListItemManager;