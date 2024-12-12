
import React, { useEffect } from "react";

// Importing components for display and configuration
import PictureAndDescriptionField from "../../../components/display/pictureAndDescriptionField/PictureAndDescriptionField";
import StoreOpeningTimesConfig from "../../../components/openingTimesConfig/StoreOpeningTimesConfig";

// Importing hooks for routing and translation
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useNavigate } from 'react-router-dom';

// Importing a text field component
import SingleLineTextField from "../../../components/display/SingleLineTextField";
import { ERR_DELETING_STORE, ERR_FETCHING_STORE, ERR_UPDATING_STORE } from "../../../constants/ErrorMessages";
import { useState } from "react";
import { SUCCESS_UPDATING_STORE } from "../../../constants/SuccessMessages";
import { BIKE_REGISTRATION } from "../../../constants/URLs/Navigation";
import { STORE_NAME } from "../../../constants/URLs/General";
import { getCookie } from "../../../services/Cookies";
import { BIKES_OF_STORE, DELETE_STORE } from "../../../constants/URIs/AdminURIs";
import { ID } from "../../../constants/URIs/General";
import { STORE_PAGE_BY_STORE_NAME } from "../../../constants/URIs/AdminURIs";
import ConfirmationPopup from '../../../components/confirmationDialog/ConfirmationPopup';
import BikeListManager from "../../../components/lists/bikeList/listVersions/BikeListManager";

// TODO make sure, storeName is passed to this component as parameter

// page for the configuration of an existing store
const StoreConfigAdmin = () => {

    const [newAddress, setNewAddress] = useState('');
    const { t } = useTranslation();
    // Hook for navigation
    const navigate = useNavigate();

    // Extracting store name from URL parameters
    const storeName = useParams().store;

    // State to hold store data
    const [store, setStore] = useState();
    const [bikes, setBikes] = useState([]);

    const token = getCookie('token');

    const [showConfirmationPopup, setShowConfirmationPopup] = useState(false);

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
                fetchBikes();
            })
            .catch(error => {
                console.error(ERR_FETCHING_STORE, error);
            });
    }

    const fetchBikes = async () => {
        const response = await fetch(BIKES_OF_STORE.replace(STORE_NAME, storeName),
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                }
            }
        );
        const data = await response.json();
        setBikes(data);
    };

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

    const deleteStore = () => {
        const payload = {}
        fetch(DELETE_STORE.replace(ID, store.id), {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                if (response) {
                    alert(t('store_deleted_successfully'));
                }
                else {
                    return response.json().then((errorText) => {
                        throw new Error(errorText.detail);
                    });
                }
            })
            .catch(error => {
                alert(ERR_DELETING_STORE + ' ' + error.message);
            })
    }

    useEffect(() => {
        fetchStore();
    }, []);

    // Handler for address change
    const handleAddressChange = (value) => {
        setNewAddress(value);
    }

    const handleCancelClick = () => {
        navigate(-1);
    }

    const handleAddBikeClick = () => {
        navigate(BIKE_REGISTRATION.replace(STORE_NAME, storeName));
    }

    // Handler for submit button click
    const handleSubmitClick = () => {
        postChanges();
    }

    const handleDeleteClick = () => {
        setShowConfirmationPopup(true);
    }

    const handlePopupConfirm = () => {
        deleteStore();
    }

    const handlePopupCancel = () => {
        setShowConfirmationPopup(false)
    }

    return (
        // not sure why this is not working withouth the condition
        <> {store ?
            <>
                <h1>{t('admin_view')}: {store.name}</h1>

                {/* Displaying store picture and description */}
                <PictureAndDescriptionField
                    image={store.image}
                    description={store.description}
                />
                {/* Single line text field for store address */}
                <SingleLineTextField editable={true} value={store.address} title={'address'} onChange={handleAddressChange} />

                {/* Configuring store opening times */}
                <StoreOpeningTimesConfig />

                <h2>{t('bikes')}</h2>
                {/* Displaying list of bikes of the store */}
                <BikeListManager bikes={bikes} />

                <div className='button-container'>
                    <button type='button' className='button regulal' onClick={handleCancelClick}>{t('cancel')}</button>
                    <button type='button' className='button regular' onClick={handleAddBikeClick}>{t('add_bike_to_store')}</button>
                    <button type='button' className='button accent' onClick={handleSubmitClick}>{t('submit_changes')}</button>
                </div>
                <div className='button-container'>
                    <button type='button' className='button accent' onClick={handleDeleteClick}>{t('delete_store')}</button>
                </div>

                <ConfirmationPopup onConfirm={handlePopupConfirm} onCancel={handlePopupCancel} show={showConfirmationPopup}>
                    {t('are_you_sure_you_want_to_delete_store') + ' ' + store.name + '?'}
                </ConfirmationPopup>
            </>
            : null}
        </>
    );
};

export default StoreConfigAdmin;