
//Item or Store in List of stores
import React from 'react';
import { useNavigate } from 'react-router-dom';

import defaultStorePicture from '../../../../assets/images/default_bike.png';
import { STORE_NAME } from '../../../../constants/URLs/General';
import { STORE_CONFIG } from '../../../../constants/URLs/Navigation';

const StoreListItemAdmin = ({ store }) => {
    const navigate = useNavigate();

    const handlePanelClick = () => {
        navigate(STORE_CONFIG.replace(STORE_NAME, store.name));
    }

    return (
        <li className='list-item' onClick={handlePanelClick}>
            <p className='list-item-label'>{store.name}</p>
            {/* TODO format properly */}
            <p className='list-item-label'>{store.address}</p>
            <div className='list-item-img-container'>
                <img className='list-item-img' alt={store.name} src={store.image ? store.image : defaultStorePicture}></img>
            </div>
        </li>
    );
};

export default StoreListItemAdmin;
