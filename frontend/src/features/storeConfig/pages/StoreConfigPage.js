
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
import { STORE } from "../../../constants/URLs/Navigation";
import { STORE_NAME } from "../../../constants/URLs/General";
import { getCookie } from "../../../services/Cookies";

// Mock data for stores (to be replaced with actual fetching logic)
// let stores = [
//     {

//         id: 1,
//         name: 'Store 1',
//         image: require('../../../assets/images/store1.jpg'),
//         description: 'This is a description of Store 1',
//         address: 'Musterstraße 123, 76137 Karlsruhe'
//     },
//     {
//         id: 2,
//         name: 'Store 2',
//         image: require('../../../assets/images/store1.jpg').default,
//         description: 'This is a description of Store 2',
//         address: 'Musterstraße 123, 76137 Karlsruhe'
//     },
//     {
//         id: 3,
//         name: 'Store 3',
//         image: null,
//         description: 'This is a description of Store 3',
//         address: 'Musterstraße 123, 76137 Karlsruhe'
//     }
// ]

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
        console.log("STORE IN FETCH", storeName)
        fetch(STORE_PAGE_BY_STORE_NAME.replace(STORE_NAME, storeName), {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
            .then(response => response.json())
            .then(data => {
                setStore(data);
                console.log("STORE", data);
            })
            .catch(error => {
                console.error(ERR_FETCHING_STORE, error);
            });
    }

    // // Function to post changes to the store
    // const postChanges = () => {
    //     let payload = {
    //         address: newAddress
    //     }
    //     fetch(STORE_PAGE_BY_STORE_NAME.replace(STORE_NAME, storeName), {
    //         method: 'PATCH',
    //         headers: {
    //             'Content-Type': 'application/json',
    //             'Authorization': `Token ${token}`
    //         },
    //         body: JSON.stringify(payload)
    //     })
    //         .then(response => response.json())
    //         .then(data => {
    //             console.log(SUCCESS_UPDATING_STORE, data);
    //         })
    //         .catch(error => {
    //             console.error(ERR_UPDATING_STORE, error);
    //         });
    // }

    useEffect(() => {
        console.log('fetching store')
        fetchStore();
    }, []);

    // Handler for address change
    const handleAddressChange = (value) => {
        setNewAddress(value);
    }

    // Handler for submit button click
    const handleSubmitClick = () => {
        // postChanges();
        navigate(STORE.replace(STORE_NAME, storeName));
    }

    return (
        <>
            {/* Displaying store picture and description */}
            <PictureAndDescriptionField
                image={store.image}
                description={store.description}
            />
            <SingleLineTextField editable={true} value={store.address} title={'address'} onChange={handleAddressChange} />
            <p>{store.address}</p>
            {/* Configuring store opening times */}
            <StoreOpeningTimesConfig />
            {/* Displaying list of bikes of the store */}
            <BikeList />
            {/* Single line text field for store name  */}
            <SingleLineTextField value={store.name} />

            <div className='button-container'>
                <button type='button' className='button regular' onClick={handleSubmitClick}>{t('submit_changes')}</button>
            </div>
        </>
    );
};

export default StoreConfigPage;