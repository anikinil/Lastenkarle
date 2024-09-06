import React, { useState, startTransition } from 'react';
import { useTranslation } from 'react-i18next';

import { useNavigate } from 'react-router-dom';

import { USER_FLAGS } from '../../../constants/URIs/AdminURIs'

const storesLst = [
    { id: 1, name: 'Store 1' },
    { id: 2, name: 'Store 2' },
    { id: 3, name: 'Store 3' },
    { id: 4, name: 'Store 4' }
]

const Enrollment = () => {

    const { t } = useTranslation();

    const navigate = useNavigate();

    const [username, setUsername] = useState();
    const [email, setEmail] = useState();

    // NOTE change when fetching implemented to:
    // const [stores, setStores] = useState([]);
    const [stores, setStores] = useState(storesLst);
    const [selectedRole, setSelectedRole] = useState({});

    // TODO token acquisition from cookie
    const [token, setToken] = useState()

    // NOTE when fetching implemented
    // const fetchStores= () => {
    //     fetch(ALL_STORES, {
    //         headers: {
    //             'Content-Type': 'application/json',
    //             'Authorization': `Token ${token}`
    //         },
    //     })
    //         .then(response => {
    //             return response.json()
    //         })
    //         .then(data => {
    //             setStores(data)
    //         })
    // }
    // useEffect(() => {
    //     fetchStores();
    // }, [])

    // THINK if variables for labels needed
    const roleOptions = [...stores.map((store) => (
        { value: store.name, label: t('manager_of') + store.name }
    )), { value: t('admin'), label: 'admin' }];

    const postEnrollment = () => {

        let payload = {
            contact_data: email,
            user_status: selectedRole
        };

        // post enrollment request
        // JAN maybe a dedicated URI for enrollment, for better encapsulation
        fetch(USER_FLAGS, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                if (response) {
                    alert(t('enrollment_successful'));
                }
                else {
                    return response.json().then((errorText) => {
                        throw new Error(errorText.detail);
                    });
                }
            })
            .catch(error => {
                // TODO proper error handling
                // TODO proper error variable
                alert('ERR_POSTING_ENROLLMENT' + ' ' + error.message);
            })
    }

    const handleRoleChange = (selectedRoleOption) => {
        setSelectedRole(selectedRoleOption.value)
    }

    // this prevents user from switching to new line by hitting [Enter]
    const handleFieldKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    };

    const handleEnrollClick = () => {
        postEnrollment()
        // TODO notify on success/failure perhaps via alert (in this line)
        // TODO add proper variable
        navigate('/')
    }

    return (
        <>
            <h1>{t('enrollment')}</h1>

            <p>{t('enter_one_of_the_following_to_identify_user')}</p>

            <textarea
                title={t('enter_username')}
                className='username'
                rows='1'
                value={username}
                onChange={e => setUsername(e.target.value)}
                onKeyDown={handleFieldKeyDown}
                placeholder={t('enter_username')}
            >
            </textarea>

            <textarea
                title={t('enter_email')}
                className='email'
                rows='1'
                value={email}
                onChange={e => setEmail(e.target.value)}
                onKeyDown={handleFieldKeyDown}
                placeholder={t('enter_email')}
            >
            </textarea>

            {/* TODO style */}

            <p>{t('select_role')}</p>
            <select title='roles' className='select' onChange={handleRoleChange}>
                {roleOptions.map(e => <option key={e.value} value={e.value}>{e.label}</option>)};
            </select>
            
            <div className='button-container'>
                <button type='button' className='button accent' onClick={handleEnrollClick}>{t('enroll')}</button>
            </div>
        </>
    );
};

export default Enrollment;