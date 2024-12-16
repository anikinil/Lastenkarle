import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import PictureAndDescriptionField from '../../../components/display/pictureAndDescriptionField/PictureAndDescriptionField';
import { useNavigate, useParams } from 'react-router-dom';
import { ERR_DELETING_BIKE, ERR_FETCHING_BIKE, ERR_UPDATING_BIKE } from '../../../constants/ErrorMessages';
import { getCookie } from '../../../services/Cookies';
import SingleLineTextField from '../../../components/display/SingleLineTextField';
import { DELETE_BIKE, UPDATE_BIKE } from '../../../constants/URIs/AdminURIs';
import { ID } from '../../../constants/URIs/General';
import { BIKE_BY_ID } from '../../../constants/URIs/RentingURIs';
import { SUCCESS_UPDATING_BIKE } from '../../../constants/SuccessMessages';
import ConfirmationPopup from '../../../components/confirmationDialog/ConfirmationPopup';

const BikeConfigAdmin = () => {
    // Hook for translation
    const { t } = useTranslation();

    // Hook for navigation
    const navigate = useNavigate()

    const token = getCookie('token')

    const [showConfirmationPopup, setShowConfirmationPopup] = useState(false);

    const bikeId = useParams().id;
    const [bike, setBike] = useState();

    const [name, setName] = useState('');
    const [pictureFile, setPictureFile] = useState(null);
    const [description, setDescription] = useState('');


    // fetches bike data
    const fetchBike = () => {
        fetch(BIKE_BY_ID.replace(ID, bikeId), {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
            .then(response => response.json())
            .then(data => {
                setBike(data);
            })
            .catch(error => {
                console.error(ERR_FETCHING_BIKE, error);
            });
    }

    useEffect(() => {
        fetchBike();
    }, [])

    // function to post changes to the bike
    const postChanges = () => {
        let payload = {
            name: name
        }
        fetch(UPDATE_BIKE.replace(ID, bike.id), {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify(payload)
        })
            .then(response => response.json())
            .then(data => {
                console.log(SUCCESS_UPDATING_BIKE, data);
            })
            .catch(error => {
                console.error(ERR_UPDATING_BIKE, error);
            });
    }

    const deleteBike = () => {
        const payload = {}
        fetch(DELETE_BIKE.replace(ID, bike.id), {
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
                alert(ERR_DELETING_BIKE + ' ' + error.message);
            })
    }

    // Handler for cancel button click
    const handleCancelClick = () => {
        // TODO maybe add a confirmation dialog
        navigate(-1)
    }

    const handleNameChange = (value) => {
        setName(value)
    }

    const handlePictureChange = (value) => {
        setPictureFile(value)
    }

    const handleDescriptionChange = (value) => {
        setDescription(value)
    }

    // Handler for register button click
    const handleConfirmClick = () => {
        postChanges();
    }

    const handleDeleteClick = () => {
        setShowConfirmationPopup(true);
    }

    const handlePopupConfirm = () => {
        deleteBike();
    }

    const handlePopupCancel = () => {
        setShowConfirmationPopup(false)
    }

    return (
        <>
        {bike ?
            <> 
                {/* Page title */}
                <h1>{t('bike_config')}: {bike.name}</h1>

                <SingleLineTextField title={t('name')} editable={true} onChange={handleNameChange} />

                {/* Picture and description field component */}
                <PictureAndDescriptionField editable={true} onPictureChange={handlePictureChange} onDescriptionChange={handleDescriptionChange} />

                {/* Button container */}
                <div className='button-container'>
                    <button type='button' className='button' onClick={handleCancelClick}>{t('cancel')}</button>
                    <button type='button' className='button accent' onClick={handleConfirmClick}>{t('confirm')}</button>
                    <button type='button' className='button accent' onClick={handleDeleteClick}>{t('delete_bike')}</button>
                </div>

                <ConfirmationPopup onConfirm={handlePopupConfirm} onCancel={handlePopupCancel} show={showConfirmationPopup}>
                    {t('are_you_sure_you_want_to_delete_bike') + ' ' + bike.name + '?'}
                </ConfirmationPopup>
            </>
            : null}
        </>
    );
};

export default BikeConfigAdmin;