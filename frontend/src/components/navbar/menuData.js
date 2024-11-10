//Structure for nav bar (drop down, structure, ...)
import React from 'react';
import { FaUser } from 'react-icons/fa';
import { ACCOUNT_DELETION, LOGIN, LOGOUT, REGIONAL_BOOKING, REGISTER } from '../../constants/URLs/Navigation';
import { REGION_NAME } from '../../constants/URLs/General';

// TODO maybe seperate into a data and a utils file

// TODO implement fetching of stores by specific owner
const stores = [
    {
        id: 1,
        name: 'Store 1'
    },
    {
        id: 2,
        name: 'Store 2'
    }
]

export const Roles = Object.freeze({
    CUSTOMER: 'Customer',
    MANAGER: 'Manager',
    ADMINISTRATOR: 'Administrator',
    VISITOR: 'Visitor'
});

const storesAsItems = stores.map((s) => ({ title: s.name, url: `/store/${s.id}` }))

// TODO make each title a translatoin constant
// TODO use URL constants for each url
export const menuItems = [
    {
        title: 'Booking',
        url: '/booking',
        roles: [Roles.CUSTOMER, Roles.MANAGER, Roles.ADMINISTRATOR, Roles.VISITOR],
        submenu: [
            {
                title: 'Karlsruhe',
                url: REGIONAL_BOOKING.replace(REGION_NAME, 'karlsruhe')
            },
            {
                title: 'Ettlingen',
                url: REGIONAL_BOOKING.replace(REGION_NAME, 'ettlingen')
            },
            {
                title: 'Bruchsaal',
                url: REGIONAL_BOOKING.replace(REGION_NAME, 'bruchsaal')
            },
            {
                title: 'Malsch',
                url: REGIONAL_BOOKING.replace(REGION_NAME, 'malsch')
            }
        ]
    },
    {
        title: 'Store management',
        url: '/stores',
        roles: [Roles.MANAGER, Roles.ADMINISTRATOR],
        submenu: storesAsItems
    },
    {
        title: 'Admin activities',
        roles: [Roles.ADMINISTRATOR],
        submenu: [
            {
                title: 'Bookings',
                url: '/bookings',
            },
            {
                title: 'Users',
                url: '/users',
            },
            {
                title: 'Stores',
                url: '/stores',
            },
            {
                title: 'Bikes',
                url: '/bikes',
            },
            {
                title: 'Enrollment',
                url: '/enrollment',
            }
        ]
    },
    {
        title: <FaUser />,
        url: '/my-bookings',
        roles: [Roles.CUSTOMER, Roles.MANAGER, Roles.ADMINISTRATOR],
        submenu: [
            {
                title: 'Logout',
                url: LOGOUT,
            },
            {
                title: 'Delete account',
                url: ACCOUNT_DELETION,
            }
        ]
    },
    {
        title: <FaUser />,
        url: null,
        roles: [Roles.VISITOR],
        submenu: [
            {
                title: 'Login',
                url: LOGIN,
            },
            {
                title: 'Register',
                url: REGISTER,
            }
        ]
    }
];