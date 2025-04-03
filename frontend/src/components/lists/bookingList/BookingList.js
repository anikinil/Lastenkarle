import React from 'react';

import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { getCookie } from '../../../services/Cookies';
import { ALL_BIKES, ALL_USERS } from '../../../constants/URIs/AdminURIs';
import BookingListItem from './BookingListItem';


const BookingList = ({ bookings }) => {

    const { t } = useTranslation();
    
    const token = getCookie('token');

    const [filteredBookings, setFilteredBookings] = useState(bookings);

    // all stores, bikes and users
    const [bikes, setBikes] = useState([])
    const [users, setUsers] = useState([])

    // select first of each list as default filter element
    const [bike, setBike] = useState()
    const [user, setUser] = useState()
    
    const fetchBikes = async () => {
        const response = await fetch(ALL_BIKES, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
            }
        });
        const data = await response.json();
        setBikes(data);
        if (data.length > 0) {
            setBike(data[0].id);
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
        if (data.length > 0) {
            setUser(data[0].username);
        }
    };

    useEffect(() => {
        fetchBikes();
        fetchUsers();
    }, [])

    useEffect(() => {
        setFilteredBookings(bookings);
    }, [bookings]);

    const handleBikeSelect = (e) => {
        setBike(e.target.value)
    }

    const handleUserSelect = (e) => {
        setUser(e.target.value)
    }

    const handleShowAllClick = () => {
        setFilteredBookings(bookings);
    }

    const handleFilterClick = () => {
        console.log(bookings)
        const filteredBookings = bookings.filter((b) => {
            return (
                b.bike == bike &&
                b.user.username == user
            )
        })
        setFilteredBookings(filteredBookings)
    }

    return (
        <>
            <div className='list-button-container'>
                {bikes.length > 0 &&
                    <select title='bikes' className='select' onChange={handleBikeSelect}>
                        {bikes.map(e => <option key={'bike' + e.name} value={e.id}>{e.name}</option>)};
                    </select>
                }
                {users.length > 0 &&
                    <select title='users' className='select' onChange={handleUserSelect}>
                        {users.map(e => <option key={'user' + e.username} value={e.username}>{e.username}</option>)};
                    </select>
                }
                {(bikes.length > 0 || users.length > 0) &&
                    <>
                        <button type='button' title={t('filter')} onClick={handleFilterClick}>{t('filter')}</button>
                        <button type='button' title={t('show_all')} onClick={handleShowAllClick}>{t('show_all')}</button>
                    </>
                }
            </div>

            <ul className='list'>
                {filteredBookings ?
                    <>
                        {filteredBookings.length > 0 ?
                            filteredBookings.map((booking) => (
                                <BookingListItem booking={booking} key={booking.id} />
                            )) : t('no_bookings')}
                    </>
                    : null}
            </ul>
        </>
    );
}

export default BookingList;