
import React, { useEffect } from "react";

// Importing components for display and configuration
import PictureAndDescriptionField from "../../../components/display/pictureAndDescriptionField/PictureAndDescriptionField";
import StoreOpeningTimesConfig from "../components/StoreOpeningTimesConfig";
import BikeList from "../../bikeList/components/BikeList";

// Importing hooks for routing and translation
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useNavigate } from 'react-router-dom';

// Importing a text field component
import SingleLineTextField from "../../../components/display/SingleLineTextField";
import { STORE_PAGE_BY_STORE_NAME } from "../../../constants/URIs/ManagerURI";
import { ERR_FETCHING_STORE, ERR_UPDATING_STORE } from "../../../constants/ErrorMessages";
import { useState } from "react";
import { SUCCESS_UPDATING_STORE } from "../../../constants/SuccessMessages";
import { BIKE_REGISTRATION, STORE } from "../../../constants/URLs/Navigation";
import { STORE_NAME } from "../../../constants/URLs/General";
import { getCookie } from "../../../services/Cookies";

// TODO make sure, storeName is passed to this component as parameter

// page for the configuration of an existing store
const StoreConfigPage = () => {

    const [newAddress, setNewAddress] = useState('');
    const { t } = useTranslation();
    // Hook for navigation
    const navigate = useNavigate();

    // Extracting store name from URL parameters
    const storeName = useParams().store;

    // State to hold store data
    const [store, setStore] = useState();

    const token = getCookie('token');

    // fetches store data
    const fetchStore = () => {
        fetch(STORE_PAGE_BY_STORE_NAME.replace(STORE_NAME, storeName), {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
            .then(response => response.json())
            .then(data => {
                setStore(data);
            })
            .catch(error => {
                console.error(ERR_FETCHING_STORE, error);
            });
    }

    // Function to post changes to the store
    const postChanges = () => {
        let payload = {
            address: newAddress
        }
        fetch(STORE_PAGE_BY_STORE_NAME.replace(STORE_NAME, storeName), {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify(payload)
        })
            .then(response => response.json())
            .then(data => {
                console.log(SUCCESS_UPDATING_STORE, data);
            })
            .catch(error => {
                console.error(ERR_UPDATING_STORE, error);
            });
    }

    useEffect(() => {
        fetchStore();
    }, []);

    // Handler for address change
    const handleAddressChange = (value) => {
        setNewAddress(value);
    }

    const handleAddBikeClick = () => {
        navigate(BIKE_REGISTRATION.replace(STORE_NAME, storeName));
    }

    // Handler for submit button click
    const handleSubmitClick = () => {
        postChanges();
        navigate(STORE.replace(STORE_NAME, storeName));
    }

    return (
        // not sure why this is not working withouth the condition
        <> {store ?
            <>
                <h1>{store.name}</h1>

                {/* Displaying store picture and description */}
                <PictureAndDescriptionField
                    image={store.image}
                    description={store.description}
                />
                {/* Single line text field for store address */}
                <SingleLineTextField editable={true} value={store.address} title={'address'} onChange={handleAddressChange} />

                {/* Configuring store opening times */}
                <StoreOpeningTimesConfig />

                {/* Displaying list of bikes of the store */}
                {/* <BikeList /> */}

                <div className='button-container'>
                    <button type='button' className='button regular' onClick={handleAddBikeClick}>{t('add_bike_to_store')}</button>
                    <button type='button' className='button accent' onClick={handleSubmitClick}>{t('submit_changes')}</button>
                </div>
            </>
            : null}
        </>
    );
};

export default StoreConfigPage;