import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css';
import BikeListItem from './BikeListItem';
import './BikeList.css'
import { FaSortAlphaDown, FaSortAlphaUp } from 'react-icons/fa';
import { useLocation, useNavigate } from 'react-router-dom';

import f from '../../../assets/images/bike1.jpg'
import { BIKES_OF_STORE, STORE_NAME } from '../../../constants/URIs/ManagerURIs';
import { getCookie } from '../../../services/Cookies';

const BikeList = ({bikes}) => {

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