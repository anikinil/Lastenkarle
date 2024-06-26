import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';


import { useNavigate } from 'react-router-dom';
import PictureAndDescriptionField from '../../../components/IO/PictureAndDescriptionField';
import AddressField from '../../../components/IO/AddressField';

const StorePage = ({ store }) => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    return (
        <>
            <h1>{store.name}</h1>

            <PictureAndDescriptionField editable={false} />
            <AddressField editable={false} />
        </>
    );
};

export default StorePage;