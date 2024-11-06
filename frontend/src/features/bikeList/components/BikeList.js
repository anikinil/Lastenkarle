import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css';
import BikeListItem from '../components/BikeListItem';
import './BikeList.css'
import { FaSortAlphaDown, FaSortAlphaUp } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

import f from '../../../assets/images/bike1.jpg'
import { BIKES_OF_STORE, STORE_NAME } from '../../../constants/URIs/ManagerURI';
import { getCookie } from '../../../services/Cookies';

const bikes = [
    {
        id: 1,
        name: 'Lastenrad 1',
        image: require('../../../assets/images/bike1.jpg'),
        description: 'This is a description of Bike 1!',
        storeId: 2
    },
    {
        id: 2,
        name: 'Lastenrad 2',
        image: require('../../../assets/images/bike2.jpg'),
        description: 'This is a description of Bike 2!',
        storeId: 3
    },
    {
        id: 3,
        name: 'Lastenrad 3',
        image: require('../../../assets/images/bike3.jpg'),
        description: 'This is a description of Bike 3!',
        storeId: 1
    },
    {
        id: 4,
        name: 'Lastenrad 4',
        image: require('../../../assets/images/bike4.jpg'),
        description: 'This is a description of Bike 4!',
        storeId: 3
    },
    {
        id: 5,
        name: 'Lastenrad 5',
        image: '',
        description: 'This is a description of Bike 5!',
        storeId: 2
    }
]

const BikeList = () => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    const [sortAZ, setSortAZ] = useState(true);

    const handleSortClick = () => {
        setSortAZ(!sortAZ)
        resort()
    }

    const resort = () => {
        bikes.sort((a, b) => sortAZ ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name))
    }

    // const [bikes, setBikes] = useState([]);

    const storeName = getCookie('store_name');
    const token = getCookie('token');

    // const fetchBikes = async () => {
    //     const response = await fetch(BIKES_OF_STORE.replace(STORE_NAME, storeName), {
    //         headers: {
    //             'Content-Type': 'application/json',
    //             'Authorization': `Token ${token}`,
    //         }
    //     });
    //     const data = await response.json();
    //     setBikes(data);
    // };

    // useEffect(() => {
    //     fetchBikes();
    // }, [])

    const handleNewBikeClick = () => {
        navigate('/bike-registration');
    }

    return (
        <>
            <div className='list-button-container'>
                <button type='button' className='sort-button' onClick={handleSortClick}>
                    {sortAZ ? <FaSortAlphaUp /> : <FaSortAlphaDown />}
                </button>
                <button type='button' className='new-bike-button' onClick={handleNewBikeClick}>{t('register_new_bike')}</button>
            </div>

            <ul className='list'>
                {bikes.map((bike) => (
                    <BikeListItem bike={bike} key={bike.id} />
                ))}
            </ul>
        </>
    );
};

export default BikeList;