import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css';
import UserListItem from '../components/UserListItem'
import './UserList.css'

import { FaSortAlphaDown, FaSortAlphaUp } from 'react-icons/fa';
import { ALL_USERS } from '../../../constants/URIs/AdminURIs';
import { getCookie } from '../../../services/Cookies';

// Component to display the list of users
const UserList = () => {

    const { t } = useTranslation();
    
    // Get the authentication token from cookies
    const token = getCookie('token');

    // State to store the list of users
    const [users, setUsers] = useState([]);

    // State to manage sorting order
    const [sortAZ, setSortAZ] = useState(true);

    // Function to fetch users from the API
    const fetchUsers = async () => {
        const response = await fetch(ALL_USERS, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
            }
        });
        const data = await response.json();
        setUsers(data);
    };

    // Fetch users when the component mounts
    useEffect(() => {
        fetchUsers();
    }, [])

    // Handle the sort button click
    const handleSortClick = () => {
        setSortAZ(!sortAZ)
        resort()
    }

    // Function to sort the users list
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
