// Import necessary libraries and components
import React, { useEffect, useState } from 'react';
import { FaSortAlphaDown, FaSortAlphaUp } from 'react-icons/fa';
import StoreListItem from './StoreListItem';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { ALL_STORES } from '../../../constants/URIs/BookingURIs';
import { getCookie } from '../../../services/Cookies';
import { STORE_REGISTRATION } from '../../../constants/URLs/Navigation';

const StoreList = () => {
    // Initialize translation and navigation hooks
    const { t } = useTranslation();
    const navigate = useNavigate();

    // Retrieve token from cookies
    const token = getCookie('token');

    // State to store the list of stores
    const [stores, setStores] = useState([]);

    // State to manage sorting order
    const [sortAZ, setSortAZ] = useState(true);

    // Function to fetch stores from the API
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

    // Fetch stores when the component mounts
    useEffect(() => {
        fetchStores();
    }, [])

    // Handle sort button click
    const handleSortClick = () => {
        setSortAZ(!sortAZ);
        resort();
    }

    // Resort the stores based on the current sorting order
    const resort = () => {
        stores.sort((a, b) => sortAZ ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name));
    }

    // Handle new store button click
    const handleNewStoreClick = () => {
        navigate(STORE_REGISTRATION);
    }

    return (
        <>
            {/* Buttons for sorting and adding new store */}
            <div className='list-button-container'>
                <button type='button' className='sort-button' onClick={handleSortClick}>
                    {sortAZ ? <FaSortAlphaUp /> : <FaSortAlphaDown />}
                </button>
                <button type='button' className='new-store-button' onClick={handleNewStoreClick}>{t('add_new_store')}</button>
            </div>

            {/* List of stores */}
            <ul className='list'>
                {stores.map((store) => (
                    <StoreListItem store={store} key={store.id} />
                ))}
            </ul>
        </>
    );
};

export default StoreList;