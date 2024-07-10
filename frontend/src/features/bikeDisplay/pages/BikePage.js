import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';


import { useNavigate, useParams } from 'react-router-dom';
import PictureAndDescriptionField from '../../../components/IO/PictureAndDescriptionField';
import BikeCalendar from '../../booking/components/calendar/BikeCalendar'
import AddressField from '../../../components/IO/AddressField';

// TODO implement fetching
//TODO: Add calandar as availability overview
const bikes = [
    {
        id: 1,
        name: 'Lastenrad 1',
        image: require('../../../assets/images/bike1.jpg'),
        description: 'This is a description of Bike 1!',
        storeId: 2
    },
    {
        id: 2,
        name: 'Lastenrad 2',
        image: require('../../../assets/images/bike2.jpg'),
        description: 'This is a description of Bike 2!',
        storeId: 3
    },
    {
        id: 3,
        name: 'Lastenrad 3',
        image: require('../../../assets/images/bike3.jpg'),
        description: 'This is a description of Bike 3!',
        storeId: 1
    },
    {
        id: 4,
        name: 'Lastenrad 4',
        image: require('../../../assets/images/bike4.jpg'),
        description: 'This is a description of Bike 4!',
        storeId: 3
    },
    {
        id: 5,
        name: 'Lastenrad 5',
        image: '',
        description: 'This is a description of Bike 5!',
        storeId: 2
    }
]
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

const BikePage = () => {

    const { t } = useTranslation();
    const navigate = useNavigate();

    const { id } = useParams();
    const bike = bikes.find(b => b.id === parseInt(id));
    const store = stores.find(s => s.id === parseInt(bike.storeId))

    const handleStoreClick = () => {
        navigate(`/store/${store.id}`)
    }

    return (
        <>
            <h1>{bike.name}</h1>

            <PictureAndDescriptionField editable={false} object={bike} />
            <AddressField editable={false} object={store} />

            <div className='button-container'>
                <button type='button' className='button regular' onClick={handleStoreClick}>{t('store')}</button>
            </div>

            <BikeCalendar />
        </>
    );
};

export default BikePage;