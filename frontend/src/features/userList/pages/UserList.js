import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import '../../../components/lists/List.css';
import UserListItem from '../components/UserListItem'
import './UserList.css'

import { FaSortAlphaDown, FaSortAlphaUp } from "react-icons/fa";

const UserList = () => {

    const { t } = useTranslation();

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
    let users = [
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

    return (
        <>
            <h1>{t('users')}</h1>

            <div className='list-button-container'>
                <button type='button' className='sort-button' title={t('sort')} onClick={handleSortClick}>
                    { sortAZ ? <FaSortAlphaDown /> : <FaSortAlphaUp />}
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