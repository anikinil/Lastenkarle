import React from 'react';
import "./Switch.css"

const Switch = ({ isOn, handleToggle }) => {

    return (
        <div className='switch'>
            <input
                checked={isOn}
                onChange={handleToggle}
                className="switch-checkbox"
                id={`switch-new`}
                type="checkbox"
            />
            <label
                className="switch-label"
                htmlFor={`switch-new`}
            >
                <span className={`switch-button`} />
            </label>
        </div>
    );
};

export default Switch;