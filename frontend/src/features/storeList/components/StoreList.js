// Import necessary libraries and components
import React, { useEffect, useState } from 'react';
import { FaSortAlphaDown, FaSortAlphaUp } from 'react-icons/fa';
import StoreListItem from './StoreListItem';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { STORE_REGISTRATION } from '../../../constants/URLs/Navigation';

const StoreList = ({ stores }) => {
    // Initialize translation and navigation hooks
    const { t } = useTranslation();
    const navigate = useNavigate();

    // State to manage sorting order
    const [sortAZ, setSortAZ] = useState(true);

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