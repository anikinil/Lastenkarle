//Page of a singular store
//TODO: Add Liste of bikes belonging to store
//Consists of Name, Picture, Description and Information
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import PictureAndDescriptionField from '../../../components/display/pictureAndDescriptionField/PictureAndDescriptionField';
import { useParams } from 'react-router-dom';
import SingleLineTextField from '../../../components/display/SingleLineTextField';
import { STORE_NAME, STORE_PAGE_BY_STORE_NAME } from '../../../constants/URIs/ManagerURI';
import { ERR_FETCHING_STORE } from '../../../constants/ErrorMessages';

const StorePage = () => {

    const { t } = useTranslation();

    const { storeName } = useParams();

    const [store, setStore] = useState();

    const fetchStore = () => {
        fetch(STORE_PAGE_BY_STORE_NAME.replace(STORE_NAME, storeName), {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
            }
        })
            .then(response => response.json())
            .then(data => {
                setStore(data);
            })
            .catch(error => {
                console.error(ERR_FETCHING_STORE, error);
            });

        useEffect(() => {
            fetchStore();
        });
    }
    
    return (
        <>
            <h1>{store.name}</h1>

            <PictureAndDescriptionField editable={false} object={store} />
            <SingleLineTextField editable={false} value={store.address} />

            {/* TODO add enrollment component for managers to enroll other managers to this particular store */}
        </>
    );
};

export default StorePage;