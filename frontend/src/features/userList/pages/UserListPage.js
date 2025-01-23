import React from "react";

import { useTranslation } from "react-i18next";
import UserList from "../../../components/lists/userList/UserList";
import { ALL_USERS } from "../../../constants/URIs/AdminURIs";
import { getCookie } from "../../../services/Cookies";
import { useEffect, useState } from "react";


const UserListPage = () => {

    const { t } = useTranslation();

    const token = getCookie('token');

    const [users, setUsers] = useState([]);
    
    // Function to fetch users from the API
    const fetchUsers = async () => {
        const response = await fetch(ALL_USERS, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
            }
        });
        const data = await response.json();
        setUsers(data.map(user => (user.username === null) ? { ...user, username: '' } : user));
    };
    
    // Fetch users when the component mounts
    useEffect(() => {
        fetchUsers();
    }, [])

    return (
        <>
            <h1>{t('users')}</h1>

            <UserList users={users} />
        </>
    );
}

export default UserListPage;