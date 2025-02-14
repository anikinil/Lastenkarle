
import React, { useEffect } from "react";

// Importing components for display and configuration
import StoreOpeningTimesConfig from "../../../components/openingTimesConfig/StoreOpeningTimesConfig";

// Importing hooks for routing and translation
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useNavigate } from 'react-router-dom';

// Importing a text field component
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

    const { t } = useTranslation();

    // Hook for navigation
    const navigate = useNavigate();

    // Extracting store name from URL parameters
    const storeName = useParams().store;

    // State to hold store data
    const [store, setStore] = useState();
    const [bikes, setBikes] = useState([]);

    const [prepareTime, setPrepareTime] = useState('');
    const [openingTimes, setOpeningTimes] = useState({});

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
                setPrepareTime(data.prep_time);
                setOpeningTimes({
                    monday: { open: data.mon_opened, from: data.mon_open, to: data.mon_close},
                    tuesday: { open: data.tue_opened, from: data.tue_open, to: data.tue_close},
                    wednesday: { open: data.wed_opened, from: data.wed_open, to: data.wed_close},
                    thursday: { open: data.thu_opened, from: data.thu_open, to: data.thu_close},
                    friday: { open: data.fri_opened, from: data.fri_open, to: data.fri_close},
                    saturday: { open: data.sat_opened, from: data.sat_open, to: data.sat_close},
                    sunday: { open: data.sun_opened, from: data.sun_open, to: data.sun_close}
                })
                console.log("STORE");
                console.log(data);
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

    // JAN time format should be HH:MM not HH:MM:SS (as it is now), to much conversion work for the frontend
    // Function to post changes to the store
    const postChanges = () => {
        let payload = {
            prepareTime: prepareTime,
            ...openingTimes
        };
        console.log(payload);
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
        fetch(DELETE_STORE.replace(STORE_NAME, store.name), {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                if (response.ok) {
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

    const handlePrepareTimeChange = (data) => {
        setPrepareTime(data);
    }

    const handleOpeningTimesChange = (data) => {
        setOpeningTimes(data)
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

                {/* Configuring store opening times */}
                <StoreOpeningTimesConfig prepareTimeValue={prepareTime} openingTimesValue={openingTimes} onPrepareTimeChange={handlePrepareTimeChange} onOpeningTimesChange={handleOpeningTimesChange} />

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