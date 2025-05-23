import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import '../../List.css'
import { FaSortAlphaDown, FaSortAlphaUp } from 'react-icons/fa';
import BikeListItemManager from '../listItemVersions/BikeListItemManager';

// displays a sortable list of provided bikes for all roles
const BikeListManager = ({ bikes }) => {

    const { t } = useTranslation();

    const [sortAZ, setSortAZ] = useState(true);

    const handleSortClick = () => {
        setSortAZ(!sortAZ)
        resort()
    }

    const resort = () => {
        bikes.sort((a, b) => sortAZ ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name))
    }

    return (
        <>
            {/* List of bikes */}
            {bikes.length === 0 ? (
                <>
                    <p>{t('no_bikes_registered')}</p>
                </>
            ) :
                <>
                    <div className='list-button-container'>
                        <button type='button' className='sort-button' onClick={handleSortClick}>
                            {sortAZ ? <FaSortAlphaUp /> : <FaSortAlphaDown />}
                        </button>
                    </div>

                    <ul className='list'>
                        {bikes.map((bike) => (
                            <BikeListItemManager bike={bike} key={bike.id} />
                        ))}
                    </ul>
                </>
            }
        </>
    );
};

export default BikeListManager;