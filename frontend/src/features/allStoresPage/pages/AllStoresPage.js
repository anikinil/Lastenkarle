// Page of a singular store
// Consists of Name, Image, Description and Information
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { getCookie } from '../../../services/Cookies';
import { ALL_STORES } from '../../../constants/URIs/AdminURIs';
import StoreListAdmin from '../../../components/lists/storeList/listVersions/StoreListAdmin';

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
            <StoreListAdmin stores={stores}/>
        </>
    );
};

export default AllStoresPage;