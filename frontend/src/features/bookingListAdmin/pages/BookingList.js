//Intended to be a component
//List of bookings
import React, { useState } from 'react';

import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css';
import BookingListItem from '../components/BookingListItem';

import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

import { ALL_BIKES, ALL_BOOKINGS, ALL_STORES, ALL_USERS } from '../../../constants/URIs/AdminURIs';
import { getCookie } from '../../../services/Cookies';

// const bookingList = [
//     {
//         id: 1,
//         date: '18.06.2024',
//         status: 'booked',
//         store: {
//             id: 1,
//             name: 'Store1'
//         },
//         bike: {
//             id: 2,
//             name: 'Lastenrad 2',
//             image: require('../../../assets/images/bike2.jpg')
//         },
//         user: {
//             id: 2,
//             name: 'alma42'
//         },
//         equipment: [],
//         comment: null
//     },
//     {
//         id: 2,
//         date: '10.05.2024',
//         status: 'picked up',
//         store: {
//             id: 2,
//             name: 'Store2'
//         },
//         bike: {
//             id: 5,
//             name: 'Lastenrad 5',
//             image: ''
//         },
//         user: {
//             id: 3,
//             name: 'alma42'
//         },
//         equipment: [],
//         comment: null
//     },
//     {
//         id: 3,
//         date: '12.05.2024',
//         status: 'booked',
//         store: {
//             id: 3,
//             name: 'Store3'
//         },
//         bike: {
//             id: 1,
//             name: 'Lastenrad 1',
//             image: require('../../../assets/images/bike1.jpg')
//         },
//         user: {
//             id: 3,
//             name: 'alma42'
//         },
//         equipment: ["Gürtel", "Helm", "Kind"],
//         comment: "suspicious activities"
//     },
//     {
//         id: 4,
//         date: '06.04.2024',
//         status: 'booked',
//         store: {
//             id: 4,
//             name: 'Store4'
//         },
//         bike: {
//             id: 3,
//             name: 'Lastenrad 3',
//             image: require('../../../assets/images/bike3.jpg')
//         },
//         user: {
//             id: 1,
//             name: 'ilja'
//         },
//         equipment: ["Helm", "Gürtel"],
//         comment: null
//     },
//     {
//         id: 5,
//         date: '22.03.2024',
//         status: 'canceled',
//         store: {
//             id: 3,
//             name: 'Store5'
//         },
//         bike: {
//             id: 3,
//             name: 'Lastenrad 1',
//             image: require('../../../assets/images/bike1.jpg')
//         },
//         user: {
//             id: 3,
//             name: 'rüdiger'
//         },
//         equipment: ["HELM"],
//         comment: "comment!"
//     }
// ]


// // should be fetched
// const stores = [
//     { key: 1, value: 'Store 1' },
//     { key: 2, value: 'Store 2' },
//     { key: 3, value: 'Store 3' },
//     { key: 4, value: 'Store 4' },
//     { key: 5, value: 'Store 5' }
// ]
// const bikes = [
//     { key: 1, value: 'Bike 1' },
//     { key: 2, value: 'Bike 2' },
//     { key: 3, value: 'Bike 3' },
//     { key: 4, value: 'Bike 4' },
//     { key: 5, value: 'Bike 5' }
// ]
// const users = [
//     { key: 1, value: 'User 1' },
//     { key: 2, value: 'User 2' },
//     { key: 3, value: 'User 3' },
//     { key: 4, value: 'User 4' },
//     { key: 5, value: 'User 5' }
// ]

const BookingList = ({ filterStore, filterBike, filterUser }) => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    const [bookings, setBookings] = useState([])

    // all stores, bikes and users
    const [stores, setStores] = useState([])
    const [bikes, setBikes] = useState([])
    const [users, setUsers] = useState([])

    // select first of each list as default filter element
    // const [store, setStore] = filterStore ? filterStore : useState(stores[0].key)
    const [store, setStore] = useState(filterStore ? filterStore : stores[0].key)
    const [bike, setBike] = useState(filterBike ? filterBike : bikes[0].key)
    const [user, setUser] = useState(filterUser ? filterUser : users[0].key)

    const token = getCookie('token')

    const fetchBookings = async () => {
        const response = await fetch(ALL_BOOKINGS, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
            }
        });
        const data = await response.json();
        setBookings(data);
    };

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

    const fetchBikes = async () => {
        const response = await fetch(ALL_BIKES, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
            }
        });
        const data = await response.json();
        setBikes(data);
    };

    const fetchUsers = async () => {
        const response = await fetch(ALL_USERS, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
            }
        });
        const data = await response.json();
        setUsers(data);
    };

    useEffect(() => {
        fetchBookings();
        fetchStores();
        fetchBikes();
        fetchUsers();
        // THINK if filtering should happen on load (in case filter parameters passed)
    })

    const handleStoreSelect = (e) => {
        setStore(e.target.value)
    }

    const handleBikeSelect = (e) => {
        setBike(e.target.value)
    }

    const handleUserSelect = (e) => {
        setUser(e.target.value)
    }

    const handleShowAllClick = () => {
        setBookings(bookings)
    }

    const handleFilterClick = () => {
        const filteredBookings = bookings.filter((b) => {
            return (
                b.store.id === store &&
                b.bike.id === bike &&
                b.user.id === user
            )
        })
        setBookings(filteredBookings)
    }

    return (
        <>
            <h1>{t('bookings')}</h1>

            <div className='list-button-container'>
                <select title='stores' className='select' onChange={handleStoreSelect}>
                    {stores.map(e => <option key={e.key} value={e.key}>{e.value}</option>)};
                </select>
                <select title='bikes' className='select' onChange={handleBikeSelect}>
                    {bikes.map(e => <option key={e.key} value={e.key}>{e.value}</option>)};
                </select>
                <select title='users' className='select' onChange={handleUserSelect}>
                    {users.map(e => <option key={e.key} value={e.key}>{e.value}</option>)};
                </select>
                <button type='button' title={t('filter')} onClick={handleFilterClick}>{t('filter')}</button>
                <button type='button' title={t('show_all')} onClick={handleShowAllClick}>{t('show_all')}</button>
            </div>

            {/* TODO make a component? */}
            <ul className='list'>
                {bookings.map((booking) => (
                    <BookingListItem booking={booking} key={booking.id} />
                ))}
            </ul>
        </>
    );
};

export default BookingList;