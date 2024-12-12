// Import necessary libraries and components
import React, { useState } from 'react';
import { FaSortAlphaDown, FaSortAlphaUp } from 'react-icons/fa';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import StoreListItemAdmin from '../listItemVersions/StoreListItemAdmin';
import { STORE_REGISTRATION } from '../../../../constants/URLs/Navigation';

const StoreListAdmin = ({ stores }) => {
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

            {stores.length === 0 ? (
                <>
                    < div className='list-button-container'>
                        <button type='button' className='new-store-button' onClick={handleNewStoreClick}>{t('add_new_store')}</button>
                    </div >
                    <p>{t('no_stores_registered')}</p>
                </>
            ) :
                <>
                    {/* Buttons for sorting and adding new store */}
                    < div className='list-button-container'>
                        <button type='button' className='sort-button' onClick={handleSortClick}>
                            {sortAZ ? <FaSortAlphaUp /> : <FaSortAlphaDown />}
                        </button>
                        <button type='button' className='new-store-button' onClick={handleNewStoreClick}>{t('add_new_store')}</button>
                    </div >
                    <ul className='list'>
                        {stores.map((store) => (
                            <StoreListItemAdmin store={store} key={store.id} />
                        ))}
                    </ul>
                </>
            }
        </>
    );
};

export default StoreListAdmin;