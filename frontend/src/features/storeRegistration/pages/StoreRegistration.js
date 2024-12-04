// Page for registering a new store
import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import './StoreRegistration.css'

import 'react-time-picker/dist/TimePicker.css';

import PictureAndDescriptionField from '../../../components/display/pictureAndDescriptionField/PictureAndDescriptionField';
import SingleLineTextField from '../../../components/display/SingleLineTextField';
import { useNavigate } from 'react-router-dom';
import { CREATE_STORE } from '../../../constants/URIs/AdminURIs';
import { getCookie } from '../../../services/Cookies';
import { ERR_FETCHING_REGIONS, ERR_POSTING_NEW_STORE } from '../../../constants/ErrorMessages';
import { REGIONS } from '../../../constants/URIs/RentingURIs';

const StoreRegistration = () => {
    
    const { t } = useTranslation(); // Translation hook
    
    const navigate = useNavigate(); // Navigation hook
    
    const handleCancelClick = () => {
        // TODO add a confirmation dialog
        navigate(-1)
    }
    
    const token = getCookie('token') // Get authentication token
    
    // State variables for form fields
    const [regionOptions, setRegionOptions] = useState([])
    const [region, setRegion] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [email, setEmail] = useState('');
    const [address, setAddress] = useState('');
    const [name, setName] = useState('');
    
    const handleRegionChange = (value) => {
        setRegion(value.target.value);
    }

    useEffect(() => {
        fetch(REGIONS, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                setRegionOptions(data.map(element => ({label: element.name, value: element.name})));
            })
            .catch(error => {
                console.error(ERR_FETCHING_REGIONS, error);
            })

    }, [])
    
    // Handlers for form field changes
    const handleNameChange = (value) => {
        setName(value)
    }
    
    const handleAddressChange = (value) => {
        setAddress(value);
    }

    const handlePhoneNumberChange = (value) => {
        setPhoneNumber(value)
    }

    const handleEmailChange = (value) => {
        setEmail(value)
    }

    // Function to post new store data to the server
    const postNewStore = () => {
        let payload = {
            region: region,
            phone_number: phoneNumber,
            email: email,
            address: address,
            name: name
        };
        return fetch(CREATE_STORE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                if (response.ok) {
                    alert(t('store_registration_successful'));
                    navigate(-1);
                } else {
                    return response.json().then((errorText) => {
                        throw new Error(errorText.detail);
                    });
                }
            })
            .catch(error => {
                alert(ERR_POSTING_NEW_STORE + ' ' + error.message);
            });
    }

    // Handler for register button click
    const handleRegisterClick = () => {
        postNewStore();
    }

    return (
        <>
            <h1>{t('new_store')}</h1>
            {/* <PictureAndDescriptionField editable={true} onDescriptionChange={}/> */}

            <p>{t('select_region')}</p>
            <select title='regions' className='select' onChange={handleRegionChange}>
                {regionOptions.map(e => <option key={e.value} value={e.value}>{e.label}</option>)}
            </select>

            <SingleLineTextField editable={true} title='name' onChange={handleNameChange} />
            <SingleLineTextField editable={true} title='address' onChange={handleAddressChange} />
            <SingleLineTextField editable={true} title='phone_number' onChange={handlePhoneNumberChange} />
            <SingleLineTextField editable={true} title='email' onChange={handleEmailChange} />

            <div className='button-container'>
                <button type='button' className='button regular' onClick={handleCancelClick}>{t('cancel')}</button>
                <button type='button' className='button accent' onClick={handleRegisterClick}>{t('register_new_store')}</button>
            </div>
        </>
    );
};

export default StoreRegistration;