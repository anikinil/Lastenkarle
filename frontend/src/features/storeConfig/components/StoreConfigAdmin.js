
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
import { BIKES_OF_STORE, DELETE_STORE, UPDATE_STORE_PAGE_BY_STORE_NAME } from "../../../constants/URIs/AdminURIs";
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
                    mon_opened: data.mon_opened, 
                    mon_open: data.mon_open,
                    mon_close: data.mon_close,
                    tue_opened: data.tue_opened,
                    tue_open: data.tue_open,
                    tue_close: data.tue_close,
                    wed_opened: data.wed_opened,
                    wed_open: data.wed_open,
                    wed_close: data.wed_close,
                    thu_opened: data.thu_opened,
                    thu_open: data.thu_open,
                    thu_close: data.thu_close,
                    fri_opened: data.fri_opened,
                    fri_open: data.fri_open,
                    fri_close: data.fri_close,
                    sat_opened: data.sat_opened,
                    sat_open: data.sat_open,
                    sat_close: data.sat_close,
                    sun_opened: data.sun_opened,
                    sun_open: data.sun_open,
                    sun_close: data.sun_close
                })
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

    const postChanges = () => {
        let payload = {
            prep_time: prepareTime,
            ...openingTimes
        };
        console.log(payload);
        fetch(UPDATE_STORE_PAGE_BY_STORE_NAME.replace(STORE_NAME, storeName), {
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

                <ConfirmationPopup onConfirm={handlePopupConfirm} onCancel={handlePopupCancel} show={showConfirmationPopup}>
                    {t('are_you_sure_you_want_to_delete_store') + ' ' + store.name + '?'}
                </ConfirmationPopup>
            </>
            : null}
        </>
    );
};

export default StoreConfigAdmin;