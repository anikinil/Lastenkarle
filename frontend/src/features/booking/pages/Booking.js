import React from "react";
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';

import FilterForAvailabilities from '../components/FilterForAvailabilities';
import AvailabilityCalendar from '../components/calendar/AvailabilityCalendar';
import BikeList from '../../bikeList/components/BikeList';

const Booking = () => {
    const { t } = useTranslation();

    const { id } = useParams();
    return (
        <>
            <h1>Booking</h1>

            <FilterForAvailabilities />
            <AvailabilityCalendar />
            <BikeList />
        </>
        
    );
};
  
export default Booking;