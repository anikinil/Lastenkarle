import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css'

import { MdDelete } from 'react-icons/md';

import defaultBikePicture from '../../../assets/images/default_bike.png'

import { useNavigate } from 'react-router-dom';
import ConfirmationPopup from '../../../components/confirmationDialog/ConfirmationPopup';
import { ALL_BOOKINGS, BIKE_RENTING } from '../../../constants/URLs/Navigation';
import { ID } from '../../../constants/URIs/General';
import { STORE_BY_BIKE_ID } from '../../../constants/URIs/RentingURIs';
import { DELETE_BIKE } from '../../../constants/URIs/AdminURIs';
import { ERR_DELETING_BIKE } from '../../../constants/ErrorMessages';
import { getCookie } from '../../../services/Cookies';

const BikeListItem = ({ bike }) => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    // THINK maybe show big preview of bike image on clik on miniature preview

    const token = getCookie('token');

    const [userRoles, setUserRoles] = useState([]);

    useEffect(() => {
        setUserRoles(getUserRoles());
    }, []);

    return (
        <>
            
        </>
    );
};

export default BikeListItem;