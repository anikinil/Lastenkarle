import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';

import { ALL_BIKES, ALL_STORES, AVAILABILITY_OF_BIKE } from '../../../constants/URIs/RentingURIs';
import { ERR_FETCHING_BIKES, ERR_FETCHING_DATA, ERR_FETCHING_STORES } from '../../../constants/messages/ErrorMessages';
import AvailabilityTable from '../components/availabilityTable/AvailabilityTable';
import FromToDatePicker from '../components/availabilityTable/FromToDatePicker';
import { ID } from '../../../constants/URIs/General';
import { getCookie } from '../../../services/Cookies';
import { useNotification } from '../../../components/notifications/NotificationContext';

//Standard page for a specific region

const RegionalRenting = () => {

    const { t } = useTranslation();

    const { showNotification } = useNotification();
    

    const token = getCookie('token');

    const regionName = useParams().region;

    const [bikes, setBikes] = useState([]);
    const [availabilities, setAvailabilities] = useState([]);

    const [from, setFrom] = useState('');
    const [to, setTo] = useState('');

    const fetchAllStores = async () => {
        try {
            const response = await fetch(ALL_STORES);
            const data = await response.json();
            return data;
        } catch (error) {
            showNotification(`${ERR_FETCHING_STORES}: ${error}`, 'error');
        }
    }

    // Fetchs all bikes
    const fetchAllBikes = async () => {
        try {
            const response = await fetch(ALL_BIKES);
            const data = await response.json();
            return data;
        } catch (error) {
            showNotification(`${ERR_FETCHING_BIKES}: ${error}`, 'error');
        }
    };

    const fetchBikeAvailabilities = async (bikeId) => {
            const response = await fetch(AVAILABILITY_OF_BIKE.replace(ID, bikeId), {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                }
            });
            const data = await response.json();
            return data;
        };

    // Filters stores by the region of the page
    const filterStoresByRegion = (allStores) => {
        return allStores.filter(store => store.region.name.toLowerCase() === regionName);
    }

    // Filters bikes by the stores in the region of the page
    const filterBikesByRegionStores = (allBikes, storesInRegion) => {
        return allBikes.filter(bike => storesInRegion.some(store => store.name === bike.store));
    }


    // useEffect hook to fetch data when the component mounts
    useEffect(() => {
        const fetchData = async () => {
            try {
                const allStores = await fetchAllStores(); // Fetch all stores
                const allBikes = await fetchAllBikes(); // Fetch all bikes
                const storesInRegion = filterStoresByRegion(allStores); // Filter stores by region
                const bikesInRegion = filterBikesByRegionStores(allBikes, storesInRegion); // Filter bikes by region stores
                setBikes(bikesInRegion); // Set bikes in state
                const bikeIds = bikesInRegion.map(bike => bike.id); // Get bike IDs
                const bikeAvailabilities = await Promise.all(bikeIds.map(fetchBikeAvailabilities)); // Fetch availabilities for each bike
                const allAvailabilities = bikeAvailabilities.flat(); // Flatten the array of availabilities
                setAvailabilities(allAvailabilities); // Set availabilities in state
            } catch (error) {
                showNotification(`${ERR_FETCHING_DATA}: ${error}`, 'error');
            }
        };
        fetchData(); // Call the fetchData function
    }, []);

    return (
        <>
            <h1>
                {t('rent_in') + ': '
                    + String(regionName[0]).toUpperCase() + String(regionName).slice(1)} {/* capitalizes region name*/}
            </h1>

            <FromToDatePicker from={from} to={to} setFrom={setFrom} setTo={setTo} />
            <AvailabilityTable bikes={bikes} availabilities={availabilities} from={from} to={to} />
        </>

    );
};

export default RegionalRenting;