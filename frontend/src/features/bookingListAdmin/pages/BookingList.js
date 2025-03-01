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
        console.log("stores", data)
        if (data.length > 0) {
            setStore(data[0].key);
        }
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
        console.log("bikes", data)
        if (data.length > 0) {
            setBike(data[0].key);
        }
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
        console.log("users", data)
        if (data.length > 0) {
            setUser(data[0].key);
        }
    };

    useEffect(() => {
        fetchStores();
        fetchBookings();
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
                {stores.length > 0 &&
                    <select title='stores' className='select' onChange={handleStoreSelect}>
                        {stores.map(e => <option key={'store' + e.name} value={e.name}>{e.name}</option>)};
                    </select>
                }
                {bikes.length > 0 &&
                    <select title='bikes' className='select' onChange={handleBikeSelect}>
                        {bikes.map(e => <option key={'bike' + e.name} value={e.name}>{e.name}</option>)};
                    </select>
                }
                {users.length > 0 &&
                    <select title='users' className='select' onChange={handleUserSelect}>
                        {users.map(e => <option key={'user' + e.username} value={e.username}>{e.username}</option>)};
                    </select>
                }
                {(stores.length > 0 || bikes.length > 0 || users.length > 0) &&
                    <>
                        <button type='button' title={t('filter')} onClick={handleFilterClick}>{t('filter')}</button>
                        <button type='button' title={t('show_all')} onClick={handleShowAllClick}>{t('show_all')}</button>
                    </>
                }
            </div>

            {/* THINK make a component? */}
            <ul className='list'>
                {bookings ?
                <>
                    {bookings.length > 0 ?
                        bookings.map((booking) => (
                            <BookingListItem booking={booking} key={booking.id} />
                        )) : t('no_bookings')}
                </>
                : null}
            </ul>
        </>
    );
};

export default BookingList;