export const menuData = [
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
    {
        title: 'Login',
        url: '/login',
        roles: ['customer', 'manager', 'admin'],
    },
];