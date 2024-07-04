import React from "react";
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';

//Standard page for a Bike
//TODO: organize Pictures
//TODO: Add bike description
//TODO: Add Store information
//TODO: Add calandar as availability overview
//TODO implement fetching
const bikes = [
    {
        id: 1,
        name: 'Lastenrad 1',
        //image: require('./bike1.jpg')
    },
    {
        id: 2,
        name: 'Lastenrad 2',
        //image: require('./bike2.jpg')
    },
    {
        id: 3,
        name: 'Lastenrad 3',
        //image: require('./bike3.jpg')
    },
    {
        id: 4,
        name: 'Lastenrad 4',
        //image: require('./bike3.jpg')
    },
    {
        id: 5,
        name: 'Lastenrad 5',
        image: ""
    }
]

const BikeBooking = () => {
    const { t } = useTranslation();

    const { id } = useParams();
    const bike = bikes.find(b => b.id === id);
    return (
        <>
            <h1>{bike.name}</h1>
        </>
    );
};

export default BikeBooking;