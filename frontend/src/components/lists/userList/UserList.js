import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css';
import UserListItem from './UserListItem';
import './UserList.css'

import { FaSortAlphaDown, FaSortAlphaUp } from 'react-icons/fa';

// Component to display the list of users
const UserList = ({ users }) => {

    const { t } = useTranslation();

    // State to manage sorting order
    const [sortAZ, setSortAZ] = useState(true);

    // Handle the sort button click
    const handleSortClick = () => {
        setSortAZ(!sortAZ)
        resort()
    }

    // Function to sort the users list
    const resort = () => {
        users.sort((a, b) => sortAZ ? a.username.localeCompare(b.username) : b.username.localeCompare(a.username))
    }

    return (
        <>
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
