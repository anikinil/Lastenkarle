import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import PictureAndDescriptionField from '../../../components/IO/PictureAndDescriptionField';
import AddressField from '../../../components/IO/AddressField';
import { useParams } from 'react-router-dom';

// TODO implement fetching
let stores = [
    {
        id: 1,
        name: 'Store 1',
        image: require('../../../assets/images/store1.jpg')
    },
    {
        id: 2,
        name: 'Store 2',
        image: require('../../../assets/images/store1.jpg')
    },
    {
        id: 3,
        name: 'Store 3',
        image: null
    }
]

const StorePage = () => {

    const { t } = useTranslation();

    const { id } = useParams();
    const store = stores.find(s => s.id === parseInt(id));

    return (
        <>
            <h1>{store.name}</h1>

            {/* TODO adjust for picture and descr display */}
            <PictureAndDescriptionField editable={false}/>
            {/* TODO adjust for address display */}
            <AddressField editable={false} />
        </>
    );
};

export default StorePage;