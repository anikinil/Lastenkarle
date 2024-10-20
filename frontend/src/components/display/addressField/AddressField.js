import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import './AddressField.css'

const AddressField = ({ editable, onChange, object }) => {

    const { t } = useTranslation();

    const handleChange = (event) => {
        onChange(event.target.value);
    };

    // this prevents user from switching to new line by hitting [Enter]
    const handleAddressFieldKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    };

    return (
        <textarea
            title={t('enter_address')}
            className='address'
            rows='1'
            value={object?.address}
            onChange={handleChange}
            onKeyDown={handleAddressFieldKeyDown}
            placeholder={t('enter_address')}
            disabled={!editable}>
        </textarea>
    );
}

export default AddressField;