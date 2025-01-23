import React, { useState } from 'react';

import './SingleLineTextField.css'

// displays a one-line textfield with information,
// which can either be changed/entered (editable=true) or just viewed (editable=false)
const SingleLineTextField = ({ editable, value, title, onChange}) => {

    const [text, setText] = useState(value);

    const handleChange = (event) => {
        setText(event.target.value);
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
            value={text}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            placeholder={title}
            disabled={!editable}>
        </textarea>
    );
}

export default SingleLineTextField;