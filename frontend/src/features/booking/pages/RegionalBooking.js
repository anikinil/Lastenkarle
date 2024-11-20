import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';

import Map from '../components/Map';
import FilterForAvailabilities from '../components/FilterForAvailabilities';
import AvailabilityCalendar from '../components/calendar/AvailabilityCalendar';
import BikeList from '../../allBikesList/components/BikeList';
import { ALL_BIKES, ALL_STORES } from '../../../constants/URIs/BookingURIs';
import { ERR_FETCHING_BIKES, ERR_FETCHING_DATA, ERR_FETCHING_STORES } from '../../../constants/ErrorMessages';
//Standard page for a specific region
//TODO: Add Map of region with station markers
//TODO: Add Filter Bar for Availabilities
//TODO: Add Calendar overview of reservations sorted by bike

const RegionalBooking = () => {

    const { t } = useTranslation();

    const regionName = useParams().region;

    const [bikesInRegion, setBikesInRegion] = useState([]);

    const fetchAllStores = async () => {
        try {
            const response = await fetch(ALL_STORES);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error(ERR_FETCHING_STORES, error);
        }
    }

    const fetchAllBikes = async () => {
        try {
            const response = await fetch(ALL_BIKES);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error(ERR_FETCHING_BIKES, error);
        }
    };

    const filterStoresByRegion = (allStores) => {
        return allStores.filter(store => store.region.name.toLowerCase() === regionName);
    }

    const filterBikesByRegionStores = (allBikes, storesInRegion) => {
        return allBikes.filter(bike => storesInRegion.some(store => store.id === bike.store));
    }

    useEffect(() => {
        const fetchData = async () => {
            try {
                // Fetch data
                const allStores = await fetchAllStores();
                const allBikes = await fetchAllBikes();

                // Filter data
                const storesInRegion = filterStoresByRegion(allStores);
                const bikesInRegion = filterBikesByRegionStores(allBikes, storesInRegion);

                // Update state
                setBikesInRegion(bikesInRegion);
            } catch (error) {
                console.error(ERR_FETCHING_DATA, error);
            }
        };

        fetchData();
    }, []);

    return (
        <>
            <h1>{t('rent_in') + ': ' + regionName}</h1>

            {/* <Map /> */}
            {/* <FilterForAvailabilities /> */}
            {/* <AvailabilityCalendar /> */}
            <BikeList bikes={bikesInRegion} />
        </>

    );
};

export default RegionalBooking;