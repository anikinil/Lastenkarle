// Shows availabilities of all bikes of all regions filtered by selected dates

import React, { useEffect } from 'react';

import { useState } from 'react';

import FromToDatePicker from '../components/FromToDatePicker';
import { ALL_AVAILABILITIES } from '../../../constants/URIs/RentingURIs';
import { getCookie } from '../../../services/Cookies';

const GeneralFilterPage = () => {

    const [availabilities, setAvailabilities] = useState([]);

    const [from, setFrom] = useState('');
    const [to, setTo] = useState('');

    const token = getCookie('token');


    const fetchAvailabilities = async () => {
            const response = await fetch(ALL_AVAILABILITIES, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                }
            });
            const data = await response.json();
            setAvailabilities(data);
        };


    useEffect(() => {
        fetchAvailabilities();
        console.log(availabilities);
    }, []);
    
    return (
        <div>
            <h1>General Filter Page</h1>

            <FromToDatePicker from={from} to={to} setFrom={setFrom} setTo={setTo} />

        </div>
    );
}

export default GeneralFilterPage;