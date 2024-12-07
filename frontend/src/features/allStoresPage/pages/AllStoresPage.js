// Page of a singular store
// TODO: Add List of bikes belonging to store
// Consists of Name, Picture, Description and Information
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { getCookie } from '../../../services/Cookies';
import StoreList from '../../../components/lists/storeList/StoreList';
import { ALL_STORES } from '../../../constants/URIs/AdminURIs';

const AllStoresPage = () => {
    const { t } = useTranslation(); // Hook for translation

    const [stores, setStores] = useState([]);

    const token = getCookie('token')

    const fetchAllStores = async () => {
        const response = await fetch(ALL_STORES,{
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,
                }
            }
        );
        const data = await response.json();
        setStores(data);
    };

    useEffect(() => {
        fetchAllStores();
    }, [])

    return (
        <>
            {/* Page title */}
            <h1>{t('stores')}</h1>

            {/* Component displaying the list of stores */}
            <StoreList stores={stores}/>
        </>
    );
};

export default AllStoresPage;