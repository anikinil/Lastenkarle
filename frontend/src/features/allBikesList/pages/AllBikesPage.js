import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css';
import BikeList from '../../../components/lists/bikeList/BikeList';
import '../../../components/lists/bikeList/BikeList.css';
import { ALL_BIKES } from '../../../constants/URIs/AdminURIs';
import { getCookie } from '../../../services/Cookies';

// AllBikesPage component definition
const AllBikesPage = () => {

    // Hook for translation
    const { t } = useTranslation();

    const token = getCookie('token');

    const [bikes, setBikes] = useState([]);

    const fetchBikes = async () => {
        const response = await fetch(ALL_BIKES,
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                }
            }
        );
        const data = await response.json();
        setBikes(data);
    };

    useEffect(() => {
        fetchBikes();
    }, []);

    return (
        <>
            {/* Page title */}
            <h1>{t('all_bikes_in_system')}</h1>

            {/* Bike list component */}
            <BikeList bikes={bikes} />
        </>
    );
};

// Export the BikeListPage component as default
export default AllBikesPage;