import React from "react";

import PictureAndDescriptionField from "../../../components/display/pictureAndDescriptionField/PictureAndDescriptionField";
import AddressField from "../../../components/display/addressField/AddressField";
import StoreOpeningTimesConfig from "../components/StoreOpeningTimesConfig";
import BikeList from "../../bikeList/components/BikeList";

import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";

import { useNavigate } from 'react-router-dom';

// TODO implement fetching
let stores = [
    {
        id: 1,
        name: 'Store 1',
        image: require('../../../assets/images/store1.jpg'),
        description: 'This is a description of Store 1',
        address: 'Musterstraße 123, 76137 Karlsruhe'
    },
    {
        id: 2,
        name: 'Store 2',
        image: require('../../../assets/images/store1.jpg').default,
        description: 'This is a description of Store 2',
        address: 'Musterstraße 123, 76137 Karlsruhe'
    },
    {
        id: 3,
        name: 'Store 3',
        image: null,
        description: 'This is a description of Store 3',
        address: 'Musterstraße 123, 76137 Karlsruhe'
    }
]

const StoreConfigPage = () => {

    const { t } = useTranslation();

    const { id } = useParams();
    const store = stores.find(s => s.id === parseInt(id));

    const navigate = useNavigate();

    const handleBookingsClick = () => {
        navigate(`/store/${id}/bookings`, {state: {id: id}})
    }

    const handleCancelClick = () => {
        // TODO maybe add a confirmation dialogue
        navigate('/stores')
    }

    const handleSaveChangesClick = () => {
        // TODO implement
    }

    return (
        <>
            <h1>{t('new_store')}</h1>
            <PictureAndDescriptionField editable={true} object={store} />
            <AddressField editable={true} object={store} />
            <StoreOpeningTimesConfig />

            <div className='button-container'>
                <button type='button' className='button regular' onClick={handleBookingsClick}>{t('bookings')}</button>
            </div>

            <h2>{t('add_bikes_to_store')}</h2>
            <BikeList />

            <div className='button-container'>
                <button type='button' className='button regular' onClick={handleBookingsClick}>{t('bookings')}</button>
                <button type='button' className='button regular' onClick={handleCancelClick}>{t('cancel')}</button>
                <button type='button' className='button accent' onClick={handleSaveChangesClick}>{t('save_changes')}</button>
            </div>
        </>
    )
}

export default StoreConfigPage;