// Component used to config the open/closed times per week day
// One row = one weekday + open-toggle + from + to + closed-toggle + from + to
import React, { useState } from 'react';
import Switch from '../switch/Switch';
import TimePicker from 'react-time-picker';
import 'react-time-picker/dist/TimePicker.css';
import '../timePicker/TimePickerCustom.css';

import { useTranslation } from 'react-i18next';

const DayRow = ({ day, isOpenValue, fromValue, toValue,  onOpenChange, onFromChange, onToChange }) => {

    const { t } = useTranslation();

    // State to manage the open toggle
    const [isOpen, setIsOpen] = useState(isOpenValue);
    // const [isOpen, setIsOpen] = useState(isOpenValue == "true" ? true : false);

    // State to manage the open from time
    const [fromTime, setFromTime] = useState(fromValue);
    // State to manage the open to time
    const [toTime, setToTime] = useState(toValue);

    // Handler for the open toggle switch
    const handleOpenChange = () => {
        setIsOpen(!isOpen) // Toggle the open state
        onOpenChange(!isOpen) // Notify the parent of the change
    }

    const handleFromChange = (time) => {
        setFromTime(time) // Update the state
        onFromChange(time) // Notify the parent of the change
    }

    const handleToChange = (time) => {
        setToTime(time) // Update the state
        onToChange(time) // Notify the parent of the change
    }

    return (
        <div className='day-row'>
            {/* Display the day label */}
            <span className='day-label'>{day}</span>
            {/* Open toggle switch */}
            <Switch id={`${day}-open`} isOn={isOpen} handleToggle={handleOpenChange} disabled={false} />
            <div>
                {/* Time picker for open from time */}
                <TimePicker
                    className='time-picker'
                    id={`${day}-open-from`}
                    onChange={handleFromChange}
                    value={fromTime}
                    disabled={!isOpen}
                    locale='de-de'
                    format='HH:mm'
                />
            </div>
            <div>
                {/* Time picker for open to time */}
                <TimePicker
                    className='time-picker'
                    id={`${day}-open-to`}
                    onChange={handleToChange}
                    value={toTime}
                    disabled={!isOpen}
                    locale='de-de'
                    format='HH:mm'
                />
            </div>
        </div>
    );
};

export default DayRow;
