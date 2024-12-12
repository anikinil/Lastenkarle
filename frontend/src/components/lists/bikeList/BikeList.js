import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import BikeListItem from './BikeListItem';
import '../List.css'
import { FaSortAlphaDown, FaSortAlphaUp } from 'react-icons/fa';

// displays a sortable list of provided bikes for all roles
const BikeList = ({ bikes }) => {

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
            <div className='list-button-container'>
                <button type='button' className='sort-button' onClick={handleSortClick}>
                    {sortAZ ? <FaSortAlphaUp /> : <FaSortAlphaDown />}
                </button>
            </div>

            {/* List of bikes */}
            {bikes.length === 0 ? (
                <p>{t('no_bikes_registered')}</p>
            ) :
                <ul className='list'>
                    {bikes.map((bike) => (
                        <BikeListItem bike={bike} key={bike.id} />
                    ))}
                </ul>
            }
        </>
    );
};

export default BikeList;