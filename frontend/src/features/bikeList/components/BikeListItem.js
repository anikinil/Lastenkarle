import React from "react";
import { useTranslation } from 'react-i18next';

import './BikeListItem.css'

import { MdDelete } from "react-icons/md";

import defaultBikePicture from "../../../assets/images/default_bike.png"

const BikeListItem = ({bike}) => {

    const { t } = useTranslation();
    
    // THINK how to display different buttons to different roles
    // THINK maybe show big preview of bike image on clik on miniature preview

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

            <button type="button" className="bike-list-item-button regular" onClick={handleBookingsClick}>{t('bookings')}</button>
            <button type="button" className="bike-list-item-button regular" onClick={handleStoreClick}>{t('store')}</button>
            <button type="button" className="bike-list-item-button delete" onClick={handleDeleteClick}>{<MdDelete />}</button>
            
            <div className="img-container">
                <img className="img" alt={bike.name} src={bike.image ? bike.image : defaultBikePicture}></img>
            </div>
        </li>
    );
};
  
export default BikeListItem;