// Shows availabilities of all bikes of all regions filtered by selected dates

import React, { useEffect } from 'react';

import { useTranslation } from 'react-i18next';

import { useState } from 'react';

import FromToDatePicker from '../components/FromToDatePicker';
import { ALL_AVAILABILITIES, ALL_BIKES, AVAILABILITY_OF_BIKE } from '../../../constants/URIs/RentingURIs';
import { getCookie } from '../../../services/Cookies';
import { ID } from '../../../constants/URIs/General';
import AvailabilityTable from '../components/AvailabilityTable';

const GeneralFilterPage = () => {

    const { t } = useTranslation();

    const token = getCookie('token');

    const [from, setFrom] = useState('');
    const [to, setTo] = useState('');

    const [bikes, setBikes] = useState([]);
    const [availabilities, setAvailabilities] = useState([]);

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


    const fetchBikes = async () => {
        const response = await fetch(ALL_BIKES, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        });
        const data = await response.json();
        setBikes(data);
    };

    // const postBooking = () => {
    //     const payload = {
    //         begin:"2025-03-12",
    //         end:"2025-03-13",
    //         equipment:[
    //         ]
    //     };

    //     fetch("http://localhost/api/booking/v1/bikes/10/booking", {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //             'Authorization': `Token ${token}`
    //         },
    //         body: JSON.stringify(payload)
    //     })
    //         .then(response => {
    //             if (response.ok) {
    //                 console.log('Booking successful');
    //             } else {
    //                 return response.json().then((errorText) => {
    //                     throw new Error(errorText.detail);
    //                 });
    //             }
    //         })
    //         .catch(error => {
    //             console.error('Error:', error);
    //         });
    // };


    useEffect(() => {
        fetchAvailabilities();
        fetchBikes();
    }, []);

    return (
        <div>
            <h1>{t('availabilities_in_all_regions')}</h1>

            <FromToDatePicker from={from} to={to} setFrom={setFrom} setTo={setTo} />
            
            <AvailabilityTable bikes={bikes} availabilities={availabilities} />
        </div>
    );
}

export default GeneralFilterPage;