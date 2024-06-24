import React from 'react';
import "./Switch.css"

const Switch = ({ id, isOn, handleToggle }) => {

    return (
        <div className='switch'>
            <input
                checked={isOn}
                onChange={handleToggle}
                className='switch-checkbox'
                id={'switch-'+id}
                type="checkbox"
            />
            <label
                className='switch-label'
                htmlFor={'switch-'+id}
            >
                <span className='switch-button' />
            </label>
        </div>
    );
};

export default Switch;