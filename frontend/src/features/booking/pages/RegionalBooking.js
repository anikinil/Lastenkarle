import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';

import Map from '../components/Map';
import FilterForAvailabilities from '../components/FilterForAvailabilities';
import AvailabilityCalendar from '../components/calendar/AvailabilityCalendar';
import BikeList from '../../allBikesList/components/BikeList';
import { ALL_BIKES, ALL_STORES } from '../../../constants/URIs/BookingURIs';
import { ERR_FETCHING_BIKES, ERR_FETCHING_STORES } from '../../../constants/ErrorMessages';
//Standard page for a specific region
//TODO: Add Map of region with station markers
//TODO: Add Filter Bar for Availabilities
//TODO: Add Calendar overview of reservations sorted by bike

const RegionalBooking = () => {

    const { t } = useTranslation();

    const regionName = useParams().region;

    const [allStores, setAllStores] = useState([]);
    const [storesInRegion, setStoresInRegion] = useState([]);
    const [allBiikes, setAllBikes] = useState([]);
    const [bikesInRegion, setBikesInRegion] = useState([]);

    const fetchAllStores = async () => {
        try {
            const response = await fetch(ALL_STORES);
            const data = await response.json();
            setAllStores(data);
            console.log(data);
        } catch (error) {
            console.error(ERR_FETCHING_STORES, error);
        }
    }

    const fetchAllBikes = async () => {
        try {
            const response = await fetch(ALL_BIKES);
            const data = await response.json();
            setAllBikes(data);
            console.log(data);
        } catch (error) {
            console.error(ERR_FETCHING_BIKES, error);
        }
    };

    const filterStoresByRegion = () => {
        setStoresInRegion(allStores.filter(store => store.region.name.toLowerCase() === regionName));
        console.log(storesInRegion);
    }

    const filterBikesByRegionStores = () => {
        setBikesInRegion(allBiikes.filter(bike => storesInRegion.some(store => store.id === bike.store)));
    }

    useEffect(() => {
        fetchAllStores();
        filterStoresByRegion();
        fetchAllBikes();
        filterBikesByRegionStores();
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