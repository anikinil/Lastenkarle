import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';


import { useNavigate, useParams } from 'react-router-dom';
import PictureAndDescriptionField from '../../../components/IO/PictureAndDescriptionField';
import BikeCalendar from '../../booking/components/calendar/BikeCalendar'
import { Descriptions } from 'antd';

// TODO implement fetching
//TODO: Add Store information
//TODO: Add calandar as availability overview
const bikes = [
    {
        id: 1,
        name: 'Lastenrad 1',
        image: require('../../../assets/images/bike1.jpg'),
        description: "This is a description of Bike 1!",
        storeId: 2
    },
    {
        id: 2,
        name: 'Lastenrad 2',
        image: require('../../../assets/images/bike2.jpg'),
        description: "This is a description of Bike 2!",
        storeId: 3
    },
    {
        id: 3,
        name: 'Lastenrad 3',
        image: require('../../../assets/images/bike3.jpg'),
        description: "This is a description of Bike 3!",
        storeId: 1
    },
    {
        id: 4,
        name: 'Lastenrad 4',
        image: require('../../../assets/images/bike4.jpg'),
        description: "This is a description of Bike 4!",
        storeId: 3
    },
    {
        id: 5,
        name: 'Lastenrad 5',
        image: "",
        description: "This is a description of Bike 5!",
        storeId: 2
    }
]

const BikePage = () => {

    const { t } = useTranslation();
    const navigate = useNavigate();

    const { id } = useParams();
    const bike = bikes.find(b => b.id === parseInt(id));

    const handleStoreClick = () => {
        navigate('/store/' + bike.storeId)
    }

    return (
        <>
            <h1>{bike.name}</h1>

            <PictureAndDescriptionField editable={false} object={bike} />

            <div className="button-container">
                <button type="button" className="button regular" onClick={handleStoreClick}>{t('store')}</button>
            </div>

            <BikeCalendar />
        </>
    );
};

export default BikePage;