//List of stores in a certain region
import React, { useState } from 'react';

import { FaSortAlphaDown, FaSortAlphaUp } from 'react-icons/fa';
import StoreListItem from './StoreListItem';

import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { ALL_STORES } from '../../../constants/URIs/BookingURIs';
import { getCookie } from '../../../services/Cookies';
import { STORE_REGISTRATION } from '../../../constants/URLs/Navigation';

const StoreList = () => {

    const { t } = useTranslation();
    const navigate = useNavigate();

    const token = getCookie('token');

    const [stores, setStores] = useState([]);

    const [sortAZ, setSortAZ] = useState(true);

    const fetchStores = async () => {
        const response = await fetch(ALL_STORES, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
            }
        });
        const data = await response.json();
        setStores(data);
    };

    useEffect(() => {
        fetchStores();
    }, [])

    const handleSortClick = () => {
        setSortAZ(!sortAZ)
        resort()
    }

    const resort = () => {
        stores.sort((a, b) => sortAZ ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name))
    }

    const handleNewStoreClick = () => {
        navigate(STORE_REGISTRATION);
    }

    return (
        <>
            <div className='list-button-container'>
                <button type='button' className='sort-button' onClick={handleSortClick}>
                    {sortAZ ? <FaSortAlphaUp /> : <FaSortAlphaDown />}
                </button>
                <button type='button' className='new-store-button' onClick={handleNewStoreClick}>{t('add_new_store')}</button>
            </div>

            <ul className='list'>
                {stores.map((store) => (
                    <StoreListItem store={store} key={store.id} />
                ))}
            </ul>
        </>
    );
};

export default StoreList;