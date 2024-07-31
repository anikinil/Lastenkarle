import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css';
import UserListItem from '../components/UserListItem'
import './UserList.css'

import { FaSortAlphaDown, FaSortAlphaUp } from 'react-icons/fa';

// TODO implement fetching
let usersLst = [
    {
        id: 1,
        name: 'ilja42',
    },
    {
        id: 2,
        name: 'alma123',
    },
    {
        id: 3,
        name: 'rüdiger',
    }
]

const UserList = () => {

    const { t } = useTranslation();
    
    const [token, setToken] = useState();

    // NOTE after fetching implemented:
    // const [users, setUsers] = useState([]);
    const [users, setUsers] = useState(usersLst);

    const [sortAZ, setSortAZ] = useState(true);


    const fetchUsers = async () => {
        const response = await fetch('URI_ADMIN_USERS', {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
            }
        });
        const data = await response.json();
        setUsers(data);
    };

    useEffect(() => {
        fetchUsers();
    }, [])

    const handleSortClick = () => {
        setSortAZ(!sortAZ)
        resort()
    }

    const resort = () => {
        users.sort((a, b) => sortAZ ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name))
    }

    return (
        <>
            <h1>{t('users')}</h1>

            <div className='list-button-container'>
                <button type='button' className='sort-button' title={t('sort')} onClick={handleSortClick}>
                    {sortAZ ? <FaSortAlphaDown /> : <FaSortAlphaUp />}
                </button>
            </div>

            <ul className='list'>
                {users.map((user) => (
                    <UserListItem user={user} key={user.id} />
                ))}
            </ul>
        </>
    );
};

export default UserList;