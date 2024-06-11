import React from "react";

import { useTranslation } from 'react-i18next';

import defaultBikePicture from "../../../assets/images/default_bike.png"

const BookingListItem = ({ booking }) => {

    const { t } = useTranslation();

    const handlePanelClick = () => {
        // TODO implement
        console.log(booking.bike.name)
    }

    const handleStoreClick = e => {
        // TODO implement
        console.log(booking.store.name)
        e.stopPropagation()
    }

    const handleUserClick = e => {
        // TODO implement
        console.log(booking.user.name)
        e.stopPropagation()
    }

    return (
        <li className="list-item" onClick={handlePanelClick}>

            <p className="list-item-label">{booking.date}</p>
            <p className="list-item-label">{booking.bike.name}</p>
            <p className="list-item-label">{booking.status}</p>

            <button type="button" className="list-item-button regular" onClick={handleStoreClick}>{booking.store.name}</button>
            <button type="button" className="list-item-button regular" onClick={handleUserClick}>{booking.user.name}</button>

            <div className="list-item-img-container">
                <img className="list-item-img" alt={booking.bike.name} src={booking.bike.image ? booking.bike.image : defaultBikePicture}></img>
            </div>
        </li>
    );
};

export default BookingListItem;