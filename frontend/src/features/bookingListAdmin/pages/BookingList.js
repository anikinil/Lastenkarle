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
    const [store, setStore] = useState()
    const [bike, setBike] = useState()
    const [user, setUser] = useState()
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
        setStore(data[0].key);
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
        setBike(data[0].key);
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
        setUser(data[0].key);
    };

    useEffect(() => {
        fetchBookings();
        fetchStores();
        fetchBikes();
        fetchUsers();
        // THINK if filtering should happen on load (in case filter parameters passed)
    }, [])

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
                {bookings ?
                bookings.map((booking) => (
                    <BookingListItem booking={booking} key={booking.id} />
                )) : null}
            </ul>
        </>
    );
};

export default BookingList;