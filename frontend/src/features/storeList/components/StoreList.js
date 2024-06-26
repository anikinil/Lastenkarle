import React, { useState } from 'react';

import { FaSortAlphaDown, FaSortAlphaUp } from "react-icons/fa";
import StoreListItem from "./StoreListItem";

import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";

// TODO implement fetching
let stores = [
    {
        id: 1,
        name: 'Store 1',
        image: require('./store1.jpg')
    },
    {
        id: 2,
        name: 'Store 2',
        image: require('./store2.jpg')
    },
    {
        id: 3,
        name: 'Store 3',
        image: null
    }
]

const StoreList = () => {

    const { t } = useTranslation();
    const navigate = useNavigate();

    const [sortAZ, setSortAZ] = useState(true);

    const handleSortClick = () => {
        setSortAZ(!sortAZ)
        resort()
    }

    const resort = () => {
        // TODO implement resorting
        console.log("resort")
    }

    const handleNewStoreClick = () => {
        navigate("/store-registration");
    }

    return (
        <>
            <div className='list-button-container'>
                <button type='button' className='sort-button' onClick={handleSortClick}>
                    {sortAZ ? <FaSortAlphaDown /> : <FaSortAlphaUp />}
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