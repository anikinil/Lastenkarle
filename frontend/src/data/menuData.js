//Structure for nav bar (drop down, structure, ...)
import React from 'react';
import { FaUser } from 'react-icons/fa';

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
    ADMIN: 'Admin',
    VISITOR: 'Visitor'
});

const storesAsItems = stores.map((s) => ({ title: s.name, url: `/store/${s.id}` }))

export const menuItems = [
    {
        title: 'Booking',
        url: '/booking',
        roles: [Roles.CUSTOMER, Roles.MANAGER, Roles.ADMIN],
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
        roles: [Roles.MANAGER, Roles.ADMIN],
        submenu: storesAsItems
    },
    {
        title: 'Admin activities',
        roles: [Roles.ADMIN],
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
        roles: [Roles.CUSTOMER, Roles.MANAGER, Roles.ADMIN],
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
        roles: [Roles.VISITOR],
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
    if (!roles || roles.length === 0) return null; // Return null or a default item if no roles are provided

    // Use a Set for faster lookups
    const rolesSet = new Set(roles);

    // Find the first matching account item configuration
    const matchingAccountItem = accountItemVersions.find(version =>
        version.roles.some(role => rolesSet.has(role))
    );

    // Return the matched item, or provide a default/fallback item for visitors if no match
    return matchingAccountItem || accountItemVersions.find(version => version.roles.includes(Roles.VISITOR));
};