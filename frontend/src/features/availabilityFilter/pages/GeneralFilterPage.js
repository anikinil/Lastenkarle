// Shows availabilities of all bikes of all regions filtered by selected dates

import React from 'react';

import FromToDatePicker from '../components/FromToDatePicker';

const GeneralFilterPage = () => {
    
    return (
        <div>
            <h1>General Filter Page</h1>

            <FromToDatePicker />
        </div>
    );
}

export default GeneralFilterPage;