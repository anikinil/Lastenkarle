import React from 'react';
import { useTranslation } from 'react-i18next';

import defaultBikeImage from '../../../../assets/images/default_bike.png'

import { useNavigate } from 'react-router-dom';
import { ID } from '../../../../constants/URIs/General';
import { getCookie } from '../../../../services/Cookies'
import { BIKE_CONFIG, STORE_DISPLAY } from '../../../../constants/URLs/Navigation';

const BikeListItemCustomer = ({ bike }) => {

    // THINK maybe show big preview of bike image on clik on miniature preview

    const { t } = useTranslation();

    const navigate = useNavigate();

    const token = getCookie('token');

    const handlePanelClick = () => {
        navigate(BIKE_CONFIG.replace(ID, bike.id));
    }

    const handleStoreClick = e => {
        navigate(STORE_DISPLAY.replace(ID, bike.store))
        e.stopPropagation()
    }

    console.log(bike)

    return (
        <>
            <li className='list-item' onClick={handlePanelClick}>

                <p className='list-item-label'>{bike.name}</p>

                <button type='button' className='list-item-button regular' onClick={handleStoreClick}>{t('store')}</button>

                <div className='list-item-img-container'>
                    <img className='list-item-img' alt={bike.name} src={bike.image ? bike.image : defaultBikeImage}></img>
                </div>
            </li>
        </>
    );
};

export default BikeListItemCustomer;