import React from 'react';
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';

import Map from '../components/Map';
import FilterForAvailabilities from '../components/FilterForAvailabilities';
import AvailabilityCalendar from '../components/calendar/AvailabilityCalendar';
import BikeList from '../../bikeList/components/BikeList';
//Standard page for a specific region
//TODO: Add Map of region with station markers
//TODO: Add Filter Bar for Availabilities
//TODO: Add Calendar overview of reservations sorted by bike
// let regions = [
//     {
//         id: 'karlsruhe',
//         name: 'Karlsruhe',
//         //bikes: [bikes in this region]
//     },
//     {
//         id: 'ettlingen',
//         name: 'Ettlingen',
//     },
//     {
//         id: 'malsch',
//         name: 'Malsch',
//     },
//     {
//         id: 'bruchsaal',
//         name: 'Bruchsaal'
//     }
// ]

const RegionalBooking = () => {
    const { t } = useTranslation();

    // const { regionName } = useParams();

    // console.log(regionName);
    // const region = regions.find(s => s.id === regionName);

    const region = {id: 'karlsruhe', name: 'Karlsruhe'}

    return (
        <>
        
            <h1>REGIONAL BOOKING</h1>
            <h1>{region.name}</h1>

            {/* <Map /> */}
            {/* <FilterForAvailabilities /> */}
            {/* <AvailabilityCalendar /> */}
            {/* <BikeList /> */}
        </>
        
    );
};
  
export default RegionalBooking;