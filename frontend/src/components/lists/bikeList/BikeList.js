import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import BikeListItem from './BikeListItem';
import '../List.css'
import { FaSortAlphaDown, FaSortAlphaUp } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

// displays a sortable list of provided bikes for all roles
const BikeList = ({bikes}) => {

    // TODO make different list components for different user roles

    const { t } = useTranslation();

    const navigate = useNavigate();

    const [sortAZ, setSortAZ] = useState(true);
    
    const handleSortClick = () => {
        setSortAZ(!sortAZ)
        resort()
    }
    
    const resort = () => {
        bikes.sort((a, b) => sortAZ ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name))
    }

    const handleNewBikeClick = () => {
        navigate('/bike-registration');
    }

    return (
        <>
            <div className='list-button-container'>
                <button type='button' className='sort-button' onClick={handleSortClick}>
                    {sortAZ ? <FaSortAlphaUp /> : <FaSortAlphaDown />}
                </button>
                <button type='button' className='new-bike-button' onClick={handleNewBikeClick}>{t('register_new_bike')}</button>
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