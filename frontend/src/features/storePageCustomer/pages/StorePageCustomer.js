// Page of a singular store
// TODO: Add List of bikes belonging to store
// Consists of Name, Image, Description and Information
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import ImageAndDescriptionField from '../../../components/display/imageAndDescriptionField/ImageAndDescriptionField';
import { useParams } from 'react-router-dom';
import SingleLineTextField from '../../../components/display/SingleLineTextField';
import { ERR_FETCHING_STORE } from '../../../constants/ErrorMessages';
import { getCookie } from '../../../services/Cookies';
import { STORE_BY_BIKE_ID } from '../../../constants/URIs/RentingURIs';
import { ID } from '../../../constants/URIs/General';

const StoreDisplay = () => {
    const { t } = useTranslation(); // Translation hook

    const bikeId = useParams().id; // Get store name from URL parameters
    const [store, setStore] = useState(); // State to hold store data

    const token = getCookie('token'); // Get authentication token from cookies

    // Function to fetch store data from the server
    const fetchStore = () => {
        fetch(STORE_BY_BIKE_ID.replace(ID, bikeId), {
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
    }, []); // Empty dependency array ensures this runs only once

    return (
        <>
            <h1>{store?.name}</h1> {/* Display store name */}

            <ImageAndDescriptionField editable={false} object={store} /> {/* Display image and description */}
            <SingleLineTextField editable={false} value={store?.address} /> {/* Display store address */}

            {/* TODO add enrollment component for managers to enroll other managers to this particular store */}
        </>
    );
};

export default StoreDisplay;