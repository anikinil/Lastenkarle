// Page of a singular store
// Consists of Name, Image, Description and Information
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import ImageAndDescriptionField from '../../../components/display/imageAndDescriptionField/ImageAndDescriptionField';
import { useParams } from 'react-router-dom';
import TextField from '../../../components/display/TextField';
import { ERR_FETCHING_STORE } from '../../../constants/messages/ErrorMessages';
import { getCookie } from '../../../services/Cookies';
import { STORE_BY_BIKE_ID } from '../../../constants/URIs/RentingURIs';
import { ID } from '../../../constants/URIs/General';
import BikeListCustomer from '../../../components/lists/bikeList/listVersions/BikeListCustomer';

const StorePageCustomer = () => {
    const { t } = useTranslation(); // Translation hook

    const bikeId = useParams().bike;
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
        <> {store &&
            <>
                <h1>{store?.name}</h1> {/* Display store name */}

                {/* NOTE crrently no image and description of store returned from backend */}
                {/* <ImageAndDescriptionField editable={false} imageValue={store?.image} descriptionValue={store?.description} /> */}
                <TextField editable={false} value={store?.address} singleLine={true} title={t('address')} /> {/* Display store address */}
            </>
        }
        </>
    );
};

export default StorePageCustomer;