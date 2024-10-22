import React from 'react';
import { useTranslation } from 'react-i18next';

import './SingleLineTextField.css'

// displays a one-line textfield with information,
// which can either be changed/entered (editable=true) or just viewed (editable=false)
const SingleLineTextField = ({ editable, value, title, onChange}) => {

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
            title={title}
            className='text-field'
            rows='1'
            value={value}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            placeholder={title}
            disabled={!editable}>
        </textarea>
    );
}

export default SingleLineTextField;