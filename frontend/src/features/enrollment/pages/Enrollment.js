// Page shown to Admins and/or managers to enroll users as admins or managers
import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';

import { USER_FLAGS } from '../../../constants/URIs/AdminURIs';
import { ALL_STORES } from '../../../constants/URIs/RentingURIs';
import { getCookie } from '../../../services/Cookies';
import { ERR_POSTING_ENROLLMENT } from '../../../constants/messages/ErrorMessages';
import { Roles } from '../../../constants/Roles';

import { useNotification } from '../../../components/notifications/NotificationContext';

const Enrollment = () => {
    const { t } = useTranslation(); // Translation hook
    const navigate = useNavigate(); // Navigation hook

    const { showNotification} = useNotification();

    // State variables
    const [email, setEmail] = useState();
    const [stores, setStores] = useState([]);
    // when role not selected, the value is ''
    const [selectedRole, setSelectedRole] = useState('');

    const token = getCookie('token'); // Get authentication token from cookies

    // Fetch stores from the server
    const fetchStores = () => {
        fetch(ALL_STORES, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
        })
            .then(response => response.json())
            .then(data => setStores(data))
            .catch(error => console.error('Error fetching stores:', error));
    };

    // Fetch stores on component mount
    useEffect(() => {
        fetchStores();
    }, []);

    // Generate role options for the select dropdown
    const roleOptions = [
        // TODO make proper store manager role parsing for API
        { value: '', label: t('not_selected') },
        { value: Roles.ADMINISTRATOR, label: Roles.ADMINISTRATOR },
        ...stores.map((store) => (
            { value: `Store: ${store.name}`, label: t('manager_of') + ' ' + store.name }
        )),
    ];

    // Post enrollment data to the server
    const postEnrollment = () => {
        const payload = {
            contact_data: email,
            flag: selectedRole
        };

        fetch(USER_FLAGS, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                if (response.ok) {
                    showNotification(t('enrollment_successful'), 'success');
                } else {
                    return response.json().then((errorText) => {
                        throw new Error(errorText.detail);
                    });
                }
            })
            .catch(error => {
                showNotification(`${ERR_POSTING_ENROLLMENT} ${error.message}`, 'error');
            });
    };

    // Handle role change in the select dropdown
    const handleRoleChange = (event) => {
        setSelectedRole(event.target.value);
    };

    // Prevent user from switching to a new line by hitting [Enter]
    const handleFieldKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    };
    
    // Handle enroll button click
    const handleEnrollClick = () => {
        if (selectedRole !== '') {
            postEnrollment();
        } else {
            showNotification('role_not_selected');
        }
    };

    const handleCancelClick = () => {
        navigate(-1);
    };

    return (
        <>
            <h1>{t('enrollment')}</h1>

            <textarea
                title={t('enter_contact_data')}
                className='email'
                rows='1'
                value={email}
                onChange={e => setEmail(e.target.value)}
                onKeyDown={handleFieldKeyDown}
                placeholder={t('enter_contact_data')}
            />

            <p>{t('select_role')}</p>
            <select title='roles' className='select' onChange={handleRoleChange}>
                {roleOptions.map(e => <option key={e.value} value={e.value}>{e.label}</option>)}
            </select>

            <div className='button-container'>
                <button type='button' className='button regular' onClick={handleCancelClick}>{t('cancel')}</button>
                <button type='button' className='button accent' onClick={handleEnrollClick}>{t('enroll')}</button>
            </div>
        </>
    );
};

export default Enrollment;
