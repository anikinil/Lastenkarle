// Import necessary libraries and components
import React, { useState } from 'react';
import { FaSortAlphaDown, FaSortAlphaUp } from 'react-icons/fa';
import { useTranslation } from 'react-i18next';
import StoreListItemManager from '../listItemVersions/StoreListItemManager';

const StoreListManager = ({ stores }) => {
    // Initialize translation and navigation hooks
    const { t } = useTranslation();

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

    return (
        <>
            {stores.length === 0 ? (
                <p>{t('no_stores_registered')}</p>

            ) :
                <>
                    {/* Buttons for sorting and adding new store */}
                    < div className='list-button-container'>
                        <button type='button' className='sort-button' onClick={handleSortClick}>
                            {sortAZ ? <FaSortAlphaUp /> : <FaSortAlphaDown />}
                        </button>
                    </div >
                    <ul className='list'>
                        {stores.map((store) => (
                            <StoreListItemManager store={store} key={store.id} />
                        ))}
                    </ul>
                </>
            }
        </>
    );
};

export default StoreListManager;