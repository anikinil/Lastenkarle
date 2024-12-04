//Page for booking (overview) across all regions and navigation between bikes and/or regions
import React from 'react';
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';

import FilterForAvailabilities from '../components/FilterForAvailabilities';
import AvailabilityCalendar from '../components/calendar/AvailabilityCalendar';

const Renting = () => {
    const { t } = useTranslation();

    const { id } = useParams();
    return (
        <>
            <h1>Renting</h1>

            {/* TODO: <ButtonsForRegions /> */}
            {/* <FilterForAvailabilities /> */}
            {/* <AvailabilityCalendar /> */}
        </>
        
    );
};
  
export default Renting;