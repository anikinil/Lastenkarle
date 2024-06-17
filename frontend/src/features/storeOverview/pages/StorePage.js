import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';


import { useNavigate } from 'react-router-dom';

const StorePage = () => {

    const { t } = useTranslation();

    const navigate = useNavigate();


    return (
        <>
            <h1>{store.name}</h1>

            
        </>
    );
};

export default StorePage;