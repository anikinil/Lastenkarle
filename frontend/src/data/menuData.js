import React from "react";
import { FaUser } from "react-icons/fa";

// TODO: maybe seperate into a data and a utils file

export const menuItems = [
    {
        title: 'Rent',
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
            },
            {
                title: 'Availabilities',
                url: '/availabilities'
            }
        ]
    },
    {
        title: 'Store management',
        url: '/store-management',
        roles: ['manager', 'admin'],
        submenu: [
            {
                title: 'Store 1',
                url: '/store1'
            },
            {
                title: 'Store 2',
                url: '/store2'
            },
            {
                title: 'Bookings in my stores',
                url: '/bookings-in-my-stores'
            }
        ]
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
        ]
    },
];

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

export const getAccountItemByRoles = (roles) => {

    return accountItemVersions.find(version => {
        return version.roles.some(role => 
            roles.includes(role))})
}