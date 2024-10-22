import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import './PhoneNumberField.css'

const PhoneNumberField = ({ editable, onChange, object }) => {

    const { t } = useTranslation();

    const handleChange = (event) => {
        onChange(event.target.value);
    };

    // this prevents user from switching to new line by hitting [Enter]
    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    };

    return (
        <textarea
            title={t('enter_phone_number')}
            className='phone_number'
            rows='1'
            value={object?.phoneNumber}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            // keyboardType='numeric'
            placeholder={t('enter_phone_number')}
            disabled={!editable}>
        </textarea>
    );
}

export default PhoneNumberField;