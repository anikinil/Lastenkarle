import React from "react";
import { useTranslation } from 'react-i18next';

import '../components/BikeListItem.css'

import { MdDelete } from "react-icons/md";

const BikeListItem = ({bike}) => {

    const { t } = useTranslation();
    
    // THINK: how to display different buttons to different roles
    return (
        <li className="list-item">
            <p className="label">{bike.name}</p>
            <button type="button" className="button regular">{t('bookings')}</button>
            <button type="button" className="button regular">{t('store')}</button>
            <button type="button" className="button delete">{<MdDelete />}</button>
            <div className="img-container">
                <img className="img" alt={bike.name} src={bike.image}></img>
            </div>
        </li>
    );
};
  
export default BikeListItem;