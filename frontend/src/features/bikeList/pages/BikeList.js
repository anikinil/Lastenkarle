import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css';
import BikeListItem from '../components/BikeListItem';
import './BikeList.css'

import { FaSortAlphaDown, FaSortAlphaUp } from "react-icons/fa";
import { useNavigate } from 'react-router-dom';

const BikeList = () => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    const [sortAZ, setSortAZ] = useState(true);

    const handleSortClick = () => {
        setSortAZ(!sortAZ)
        resort()
    }

    const resort = () => {
        // TODO implement resorting
        console.log("resort")
    }

    const handleNewBikeClick = () => {
        navigate("/bike-registration");
    }

    // TODO implement fetching
    let bikes = [
        {
            id: 1,
            name: 'Lastenrad 1',
            image: require('./bike1.jpg')
        },
        {
            id: 2,
            name: 'Lastenrad 2',
            image: require('./bike2.jpg')
        },
        {
            id: 3,
            name: 'Lastenrad 3',
            image: require('./bike3.jpg')
        },
        {
            id: 4,
            name: 'Lastenrad 4',
            image: require('./bike3.jpg')
        },
        {
            id: 5,
            name: 'Lastenrad 5',
            image: ""
        }
    ]

    return (
        <>
            <h1>{t('bikes')}</h1>

            <div className='list-button-container'>
                <button type='button' className='sort-button' onClick={handleSortClick}>
                    { sortAZ ? <FaSortAlphaDown /> : <FaSortAlphaUp />}
                </button>
                <button type='button' className='new-bike-button' onClick={handleNewBikeClick}>{t('add_new_bike')}</button>
            </div>

            <ul className='list'>
                {bikes.map((bike) => (
                    <BikeListItem bike={bike} key={bike.id} />
                ))}
            </ul>
        </>
    );
};

export default BikeList;