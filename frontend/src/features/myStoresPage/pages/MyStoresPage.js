
import React, { useEffect, useState } from 'react';
import StoreList from '../../storeList/components/StoreList';
import { useTranslation } from 'react-i18next';
import { getCookie } from '../../../services/Cookies';
import { MY_STORES } from '../../../constants/URIs/ManagerURIs';

const MyStoresPage = () => {
    const { t } = useTranslation(); // Hook for translation

    const [stores, setStores] = useState([]);

    const token = getCookie('token')

    const fetchMyStores = async () => {
        // TODO wait till Jan adds the call
        const response = await fetch(MY_STORES,{
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
        fetchMyStores();
    }, [])

    return (
        <>
            {/* Page title */}
            <h1>{t('my_stores')}</h1>

            {/* Component displaying the list of stores */}
            <StoreList stores={stores}/>
        </>
    );
};

export default MyStoresPage;