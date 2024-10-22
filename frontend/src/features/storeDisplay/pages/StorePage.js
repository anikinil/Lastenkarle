//Page of a singular store
//TODO: Add Liste of bikes belonging to store
//Consists of Name, Picture, Description and Information
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import PictureAndDescriptionField from '../../../components/display/pictureAndDescriptionField/PictureAndDescriptionField';
import { useParams } from 'react-router-dom';
import SingleLineTextField from '../../../components/display/SingleLineTextField';

// TODO implement fetching
let stores = [
    {
        id: 1,
        name: 'Store 1',
        image: require('../../../assets/images/store1.jpg'),
        description: 'This is a description of Store 1',
        address: 'Musterstraße 123, 76137 Karlsruhe'
    },
    {
        id: 2,
        name: 'Store 2',
        image: require('../../../assets/images/store1.jpg').default,
        description: 'This is a description of Store 2',
        address: 'Musterstraße 123, 76137 Karlsruhe'
    },
    {
        id: 3,
        name: 'Store 3',
        image: null,
        description: 'This is a description of Store 3',
        address: 'Musterstraße 123, 76137 Karlsruhe'
    }
]

const StorePage = () => {

    const { t } = useTranslation();

    const { id } = useParams();
    const store = stores.find(s => s.id === parseInt(id));

    return (
        <>
            <h1>{store.name}</h1>

            <PictureAndDescriptionField editable={false} object={store}/>
            <SingleLineTextField editable={false} value={store.address}/>

            {/* TODO add enrollment component for managers to enroll other managers to this particular store */}
        </>
    );
};

export default StorePage;