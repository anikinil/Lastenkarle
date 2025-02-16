// Component used to config the open/closed times per week day
// One row = one weekday + open-toggle + from + to + closed-toggle + from + to
import React, { useState } from 'react';
import Switch from '../switch/Switch';
import TimePicker from 'react-time-picker';
import 'react-time-picker/dist/TimePicker.css';
import '../timePicker/TimePickerCustom.css';

import { useTranslation } from 'react-i18next';

const DayRow = ({ day, onOpenChange, onFromChange, onToChange }) => {

    const { t } = useTranslation();

    // State to manage the open toggle
    const [isOpen, setIsOpen] = useState(false);

    // State to manage the open from time
    const [openFromTime, setOpenFromTime] = useState(t('placeholder_open_from_time'));
    // State to manage the open to time
    const [openToTime, setOpenToTime] = useState(t('placeholder_open_to_time'));

    // Handler for the open toggle switch
    const handleOpenChange = () => {
        setIsOpen(!isOpen) // Toggle the open state
        onOpenChange(!isOpen) // Notify the parent of the change
    }

    const handleFromChange = (time) => {
        setOpenFromTime(time) // Update the state
        onFromChange(time) // Notify the parent of the change
    }

    const handleToChange = (time) => {
        setOpenToTime(time) // Update the state
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
                    value={openFromTime}
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
                    value={openToTime}
                    disabled={!isOpen}
                    locale='de-de'
                    format='HH:mm'
                />
            </div>
        </div>
    );
};

export default DayRow;
