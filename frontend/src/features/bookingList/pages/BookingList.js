import React, { useState } from 'react';

import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css';
import BookingListItem from '../components/BookingListItem';

import { useNavigate } from 'react-router-dom';

// TODO implement fetching
const bookingList = [
    {
        id: 1,
        date: "18.06.2024",
        status: "booked",
        store: {
            id: 1,
            name: 'Store1'
        },
        bike: {
            id: 2,
            name: 'Lastenrad 2',
            image: require('./bike2.jpg')
        },
        user: {
            id: 2,
            name: 'alma42'
        }
    },
    {
        id: 2,
        date: "10.05.2024",
        status: "picked up",
        store: {
            id: 2,
            name: 'Store2'
        },
        bike: {
            id: 5,
            name: 'Lastenrad 5',
            image: ""
        },
        user: {
            id: 3,
            name: 'alma42'
        }
    },
    {
        id: 3,
        date: "12.05.2024",
        status: "booked",
        store: {
            id: 3,
            name: 'Store3'
        },
        bike: {
            id: 1,
            name: 'Lastenrad 1',
            image: require('./bike1.jpg')
        },
        user: {
            id: 3,
            name: 'alma42'
        }
    },
    {
        id: 4,
        date: "06.04.2024",
        status: "booked",
        store: {
            id: 4,
            name: 'Store4'
        },
        bike: {
            id: 3,
            name: 'Lastenrad 3',
            image: require('./bike3.jpg')
        },
        user: {
            id: 1,
            name: 'ilja'
        }
    },
    {
        id: 5,
        date: "22.03.2024",
        status: "canceled",
        store: {
            id: 3,
            name: 'Store5'
        },
        bike: {
            id: 3,
            name: 'Lastenrad 1',
            image: require('./bike1.jpg')
        },
        user: {
            id: 3,
            name: 'rüdiger'
        }
    }
]


// should be fetched
const stores = [
    { key: 1, value: 'Store 1' },
    { key: 2, value: 'Store 2' },
    { key: 3, value: 'Store 3' },
    { key: 4, value: 'Store 4' },
    { key: 5, value: 'Store 5' }
]
const bikes = [
    { key: 1, value: 'Bike 1' },
    { key: 2, value: 'Bike 2' },
    { key: 3, value: 'Bike 3' },
    { key: 4, value: 'Bike 4' },
    { key: 5, value: 'Bike 5' }
]
const users = [
    { key: 1, value: 'User 1' },
    { key: 2, value: 'User 2' },
    { key: 3, value: 'User 3' },
    { key: 4, value: 'User 4' },
    { key: 5, value: 'User 5' }
]

const BookingList = () => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    const [bookings, setBookings] = useState(bookingList)

    const [store, setStore] = useState(stores[0].key)
    const [bike, setBike] = useState(bikes[0].key)
    const [user, setUser] = useState(users[0].key)

    const handleStoreSelect = (e) => {
        setStore(e.target.value)
        console.log(store)
    }

    const handleBikeSelect = (e) => {
        setBike(e.target.value)
        console.log(bike)
    }

    const handleUserSelect = (e) => {
        setUser(e.target.value)
        console.log(user)
    }

    const handleShowAllClick = () => {
        setBookings(bookingList)
    }

    const handleFilterClick = () => {

        const filteredBookings = bookingList.filter((b) => {
            return (
                b.store.id == store &&
                b.bike.id == bike &&
                b.user.id == user
            )
        })

        setBookings(filteredBookings)
    }


    return (
        <>
            <h1>{t('bookings')}</h1>

            <div className='list-button-container'>
                <select title="stores" className='select' onChange={handleStoreSelect}>
                    {stores.map(e => <option key={e.key} value={e.key}>{e.value}</option>)};
                </select>
                <select title="bikes" className='select' onChange={handleBikeSelect}>
                    {bikes.map(e => <option key={e.key} value={e.key}>{e.value}</option>)};
                </select>
                <select title="users" className='select' onChange={handleUserSelect}>
                    {users.map(e => <option key={e.key} value={e.key}>{e.value}</option>)};
                </select>
                <button type='button' title={t('filter')} onClick={handleFilterClick}>{t('filter')}</button>
                <button type='button' title={t('show_all')} onClick={handleShowAllClick}>{t('show_all')}</button>
            </div>

            <ul className='list'>
                {bookings.map((booking) => (
                    <BookingListItem booking={booking} key={booking.id} />
                ))}
            </ul>
        </>
    );
};

export default BookingList;