//Structure for nav bar (drop down, structure, ...)
import React from 'react';
import { FaUser } from 'react-icons/fa';

// TODO: maybe seperate into a data and a utils file

// TODO: implement fetching of stores by specific owner
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

const storesAsItems = stores.map((s) => ({ title: s.name, url: `/store/${s.id}` }))

export const menuItems = [
    {
        title: 'Booking',
        url: '/booking',
        roles: ['customer', 'manager', 'admin'],
        submenu: [
            {
                title: 'Karlsruhe',
                url: '/karlsruhe'
            },
            {
                title: 'Ettlingen',
                url: '/ettlingen'
            },
            {
                title: 'Bruchsaal',
                url: '/bruchsaal'
            },
            {
                title: 'Malsch',
                url: '/malsch'
            }
        ]
    },
    {
        title: 'Store management',
        url: '/stores',
        roles: ['manager', 'admin'],
        submenu: storesAsItems
    },
    {
        title: 'Admin activities',
        roles: ['admin'],
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
];

// TODO implement logout properly
const accountItemVersions = [
    {
        title: <FaUser />,
        url: '/login',
        roles: ['customer', 'manager', 'admin'],
        submenu: [
            {
                title: 'My bookings',
                url: '/my-bookings',
            },
            {
                title: 'Logout',
                url: '/logout',
            }
        ]
    },
    {
        title: <FaUser />,
        url: '/login',
        roles: ['visitor'],
        submenu: [
            {
                title: 'My bookings',
                url: '/my-bookings',
            },
            {
                title: 'Register',
                url: '/register',
            },
            {
                title: 'Login',
                url: '/login',
            }
        ]
    }
]

console.log(menuItems)

export const getAccountItemByRoles = (roles) => {

    return accountItemVersions.find(version => {
        return version.roles.some(role =>
            roles.includes(role))
    })
}