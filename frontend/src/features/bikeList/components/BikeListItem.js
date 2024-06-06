import React from "react";
import { useTranslation } from 'react-i18next';

import '../components/BikeListItem.css'

import { MdDelete } from "react-icons/md";

const BikeListItem = ({bike}) => {

    const { t } = useTranslation();
    
    // THINK how to display different buttons to different roles
    // THINK maybe show big preview of bike image on lcik on miniature preview

    const handlePanelClick = () => {
        // TODO implement
        console.log(bike.name)
    }

    const handleBookingsClick = e => {
        // TODO implement
        console.log("bookings")
        e.stopPropagation()
    }

    const handleStoreClick = e => {
        // TODO implement
        console.log("store")
        e.stopPropagation()
    }

    const handleDeleteClick = e => {
        // TODO implement
        console.log("delete")
        e.stopPropagation()
    }

    return (
        <li className="list-item" onClick={handlePanelClick}>
            <p className="label">{bike.name}</p>
            <button type="button" className="button regular" onClick={handleBookingsClick}>{t('bookings')}</button>
            <button type="button" className="button regular" onClick={handleStoreClick}>{t('store')}</button>
            <button type="button" className="button delete" onClick={handleDeleteClick}>{<MdDelete />}</button>
            <div className="img-container">
                <img className="img" alt={bike.name} src={bike.image}></img>
            </div>
        </li>
    );
};
  
export default BikeListItem;