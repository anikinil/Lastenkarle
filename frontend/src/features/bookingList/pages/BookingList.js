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

    const [sortAZ, setSortAZ] = useState(true);

    const handleSortClick = () => {
        setSortAZ(!sortAZ)
        resort()
    }

    const resort = () => {
        // TODO implement resorting
        console.log("resort")
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
                <button type='button' className='sort-button' onClick={handleSortClick}>
                    {sortAZ ? <FaSortAlphaDown /> : <FaSortAlphaUp />}
                </button>
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