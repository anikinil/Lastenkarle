import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import { useNavigate } from 'react-router-dom';

const BikeListItemCustomer = ({ bike }) => {

    const { t } = useTranslation();

    const navigate = useNavigate();

   
    return (
        <>
            <p>CUSTOMER</p>
        </>
    );
};

export default BikeListItemCustomer;