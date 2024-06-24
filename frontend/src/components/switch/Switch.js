import React from 'react';
import "./Switch.css"

const Switch = ({ id, isOn, handleToggle, disabled }) => {

    return (
        <div className='switch'>
            <input
                checked={isOn}
                onChange={handleToggle}
                className='switch-checkbox'
                id={`switch-${id}`}
                type="checkbox"
                disabled={disabled}
                />
            <label
                className='switch-label'
                htmlFor={`switch-${id}`}
                disabled={disabled}
                >
                <span className='switch-button' />
            </label>
        </div>
    );
};

export default Switch;