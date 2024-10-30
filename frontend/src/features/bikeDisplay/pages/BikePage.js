//Page of singular Bike
//Consists of a Name, Picture, Description and Information about the store it belongs to
//Also has BikeCalendar which is component to make a reservation
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate, useParams } from 'react-router-dom';
import PictureAndDescriptionField from '../../../components/display/pictureAndDescriptionField/PictureAndDescriptionField';
import SingleLineTextField from '../../../components/display/SingleLineTextField';
import BikeCalendar from '../../booking/components/calendar/BikeCalendar';
import { ID } from '../../../constants/URIs/General';
import { BIKE_BY_ID, STORE_BY_BIKE_ID } from '../../../constants/URIs/BookingURIs';
import { ERR_FETCHING_BIKE, ERR_FETCHING_STORE } from '../../../constants/ErrorMessages';

const BikePage = () => {

    const { t } = useTranslation();
    const navigate = useNavigate();

    const { id } = useParams();
    const [bike, setBike] = useState();
    const [store, setStore] = useState();

    const fetchBike = () => {
        fetch(BIKE_BY_ID.replace(ID, id), {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
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

    const fetchStore = () => {
        fetch(STORE_BY_BIKE_ID.replace(ID, id), {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
            }
        })
            .then(response => response.json())
            .then(data => {
                setStore(data);
            })
            .catch(error => {
                console.error(ERR_FETCHING_STORE, error);
            });

        useEffect(() => {
            fetchStore();
        });
    }

    useEffect(() => {
        fetchBike();
        fetchStore();
    }, [])

    const handleStoreClick = () => {
        navigate(`/store/${store.id}`)
    }

    return (
        <>
            <h1>{bike.name}</h1>

            <PictureAndDescriptionField editable={false} object={bike} />
            <SingleLineTextField editable={false} value={store.address} title='address' />

            <div className='button-container'>
                <button type='button' className='button regular' onClick={handleStoreClick}>{t('store')}</button>
            </div>

            <BikeCalendar />
        </>
    );
};

export default BikePage;