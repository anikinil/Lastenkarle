import React from 'react';
import { useTranslation } from 'react-i18next';

import defaultBikeImage from '../../../../assets/images/default_bike.png'

import { useNavigate } from 'react-router-dom';
import { HOST, ID } from '../../../../constants/URIs/General';
import { getCookie } from '../../../../services/Cookies'
import { BIKE_RENTING, STORE_DISPLAY } from '../../../../constants/URLs/Navigation';
import { STORE_NAME } from '../../../../constants/URLs/General';

const BikeListItemCustomer = ({ bike }) => {

    // THINK maybe show big preview of bike image on clik on miniature preview

    const { t } = useTranslation();

    const navigate = useNavigate();

    const handlePanelClick = () => {
        navigate(BIKE_RENTING.replace(ID, bike.id));
    }

    const handleStoreClick = e => {
        navigate(STORE_DISPLAY.replace(STORE_NAME, bike.store))
        e.stopPropagation()
    }

    return (
        <>
            <li className='list-item' onClick={handlePanelClick}>

                <p className='list-item-label'>{bike.name}</p>

                <button type='button' className='list-item-button regular' onClick={handleStoreClick}>{t('store')}</button>

                <div className='list-item-img-container'>
                    <img className='list-item-img' alt={bike.name} src={bike.image ? HOST + bike.image : defaultBikeImage}></img>
                </div>
            </li>
        </>
    );
};

export default BikeListItemCustomer;