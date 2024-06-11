import React, { useState } from 'react';

import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css';
import BookingListItem from '../components/BookingListItem';
import './BookingList.css'

import { FaSortAlphaDown, FaSortAlphaUp } from "react-icons/fa";
import { useNavigate } from 'react-router-dom';

const BookingList = () => {

    const { t } = useTranslation();

    const navigate = useNavigate();


    const stores = [
        { key: 'Store1', value: 'Store1' },
        { key: 'Store2', value: 'Store2' },
        { key: 'Store3', value: 'Store3' },
        { key: 'Store4', value: 'Store4' },
        { key: 'Store5', value: 'Store5' }
    ]

    const bikes = [
        { key: 'Bike1', value: 'Bike1' },
        { key: 'Bike2', value: 'Bike2' },
        { key: 'Bike3', value: 'Bike3' },
        { key: 'Bike4', value: 'Bike4' },
        { key: 'Bike5', value: 'Bike5' }
    ]

    const users = [
        { key: 'User1', value: 'User1' },
        { key: 'User2', value: 'User2' },
        { key: 'User3', value: 'User3' },
        { key: 'User4', value: 'User4' },
        { key: 'User5', value: 'User5' }
    ]


    const handleFilterClick = () => {
        // TODO implement resorting
        console.log("filter")
    }

    // TODO implement fetching
    let bookings = [
        {
            id: 1,
            date: "18.06.2024",
            status: "booked",
            bike: {
                id: 2,
                name: 'Lastenrad 2',
                image: require('./bike2.jpg')
            },
            store: {
                name: 'Store1'
            },
            user: {
                name: 'alma42'
            }
        },
        {
            id: 2,
            date: "10.05.2024",
            status: "picked up",
            bike: {
                id: 5,
                name: 'Lastenrad 5',
                image: ""
            },
            store: {
                name: 'Store2'
            },
            user: {
                name: 'alma42'
            }
        },
        {
            id: 3,
            date: "12.05.2024",
            status: "booked",
            bike: {
                id: 1,
                name: 'Lastenrad 1',
                image: require('./bike1.jpg')
            },
            store: {
                name: 'Store3'
            },
            user: {
                name: 'alma42'
            }
        },
        {
            id: 4,
            date: "06.04.2024",
            status: "booked",
            bike: {
                id: 3,
                name: 'Lastenrad 3',
                image: require('./bike3.jpg')
            },
            store: {
                name: 'Store4'
            },
            user: {
                name: 'ilja'
            }
        },
        {
            id: 5,
            date: "22.03.2024",
            status: "canceled",
            bike: {
                id: 1,
                name: 'Lastenrad 1',
                image: require('./bike1.jpg')
            },
            store: {
                name: 'Store5'
            },
            user: {
                name: 'rüdiger'
            }
        }
    ]

    return (
        <>
            <h1>{t('bookings')}</h1>

            <div className='list-button-container'>
                <select title="stores">
                    {stores.map(e => <option key={e.key} value={e.key}>{e.value}</option>)};
                </select>
                <select title="bikes">
                    {bikes.map(e => <option key={e.key} value={e.key}>{e.value}</option>)};
                </select>
                <select title="users">
                    {users.map(e => <option key={e.key} value={e.key}>{e.value}</option>)};
                </select>
                <button type='button' className='button regular' onClick={handleFilterClick}>{t('filter')}</button>
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