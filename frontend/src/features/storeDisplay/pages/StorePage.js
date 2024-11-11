// Page of a singular store
// TODO: Add List of bikes belonging to store
// Consists of Name, Picture, Description and Information
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import PictureAndDescriptionField from '../../../components/display/pictureAndDescriptionField/PictureAndDescriptionField';
import { useParams } from 'react-router-dom';
import SingleLineTextField from '../../../components/display/SingleLineTextField';
import { STORE_NAME, STORE_PAGE_BY_STORE_NAME } from '../../../constants/URIs/ManagerURI';
import { ERR_FETCHING_STORE } from '../../../constants/ErrorMessages';
import { getCookie } from '../../../services/Cookies';

const StorePage = () => {
    const { t } = useTranslation(); // Translation hook

    const { storeName } = useParams(); // Get store name from URL parameters
    const [store, setStore] = useState(); // State to hold store data

    const token = getCookie('token'); // Get authentication token from cookies

    // Function to fetch store data from the server
    const fetchStore = () => {
        fetch(STORE_PAGE_BY_STORE_NAME.replace(STORE_NAME, storeName), {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
            }
        })
            .then(response => response.json()) // Parse JSON response
            .then(data => {
                setStore(data); // Set store data to state
            })
            .catch(error => {
                console.error(ERR_FETCHING_STORE, error); // Log error if fetching fails
            });
    }

    // Fetch store data when component mounts
    useEffect(() => {
        fetchStore();
    }); // Empty dependency array ensures this runs only once

    return (
        <>
            <h1>{store.name}</h1> {/* Display store name */}

            <PictureAndDescriptionField editable={false} object={store} /> {/* Display picture and description */}
            <SingleLineTextField editable={false} value={store.address} /> {/* Display store address */}

            {/* TODO add enrollment component for managers to enroll other managers to this particular store */}
        </>
    );
};

export default StorePage;