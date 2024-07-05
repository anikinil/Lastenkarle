import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';


import { useNavigate, useParams } from 'react-router-dom';
import PictureAndDescriptionField from '../../../components/IO/PictureAndDescriptionField';

// TODO implement fetching
//TODO: Add Store information
//TODO: Add calandar as availability overview
const bikes = [
    {
        id: 1,
        name: 'Lastenrad 1',
        image: require('../../../assets/images/bike1.jpg')
    },
    {
        id: 2,
        name: 'Lastenrad 2',
        image: require('../../../assets/images/bike2.jpg')
    },
    {
        id: 3,
        name: 'Lastenrad 3',
        image: require('../../../assets/images/bike3.jpg')
    },
    {
        id: 4,
        name: 'Lastenrad 4',
        image: require('../../../assets/images/bike4.jpg')
    },
    {
        id: 5,
        name: 'Lastenrad 5',
        image: ""
    }
]

const BikePage = () => {

    const { t } = useTranslation();
    const navigate = useNavigate();

    const { id } = useParams();
    const bike = bikes.find(b => b.id === parseInt(id));

    return (
        <>
            <h1>{bike.name}</h1>

            <PictureAndDescriptionField editable={false}/>
        </>
    );
};

export default BikePage;