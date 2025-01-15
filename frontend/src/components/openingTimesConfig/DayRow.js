// Component used to config the open/closed times per week day
// One row = one weekday + open-toggle + from + to + closed-toggle + from + to
import React, { useState } from 'react';
import Switch from '../switch/Switch';
import TimePicker from 'react-time-picker';
import 'react-time-picker/dist/TimePicker.css';
import '../timePicker/TimePickerCustom.css';

import { useTranslation } from 'react-i18next';

const DayRow = ({ day, onChange }) => {

    const { t } = useTranslation();

    // State to manage the open toggle
    const [isOpen, setIsOpen] = useState(false);
    // State to manage the closed toggle
    const [isClosed, setIsClosed] = useState(false);

    // State to manage the open from time
    const [openFromTime, setOpenFromTime] = useState(t('placeholder_open_from_time'));
    // State to manage the open to time
    const [openToTime, setOpenToTime] = useState(t('placeholder_open_to_time'));
    // State to manage the closed from time
    const [closedFromTime, setClosedFromTime] = useState(t('placeholder_closed_from_time'));
    // State to manage the closed to time
    const [closedToTime, setClosedToTime] = useState(t('placeholder_closed_to_time'));

    // Handler for the open toggle switch
    const handleOpenToggle = () => {
        if (isOpen) { setIsClosed(false) } // If open is toggled off, also turn off closed
        setIsOpen(!isOpen) // Toggle the open state
    }

    // Handler for the closed toggle switch
    const handleClosedToggle = () => {
        setIsClosed(!isClosed) // Toggle the closed state
    }

    return (
        <div className='day-row'>
            {/* Display the day label */}
            <span className='day-label'>{day}</span>
            {/* Open toggle switch */}
            <Switch id={`${day}-open`} isOn={isOpen} handleToggle={handleOpenToggle} disabled={false} />
            <div>
                {/* Time picker for open from time */}
                <TimePicker
                    className='time-picker'
                    id={`${day}-open-from`}
                    onChange={setOpenFromTime}
                    value={openFromTime}
                    disabled={!isOpen}
                    locale='de-de'
                />
            </div>
            <div>
                {/* Time picker for open to time */}
                <TimePicker
                    className='time-picker'
                    id={`${day}-open-to`}
                    onChange={setOpenToTime}
                    value={openToTime}
                    disabled={!isOpen}
                    locale='de-de'
                />
            </div>

            {/* Closed toggle switch */}
            <Switch id={`${day}-closed`} isOn={isClosed} handleToggle={handleClosedToggle} disabled={!isOpen} />
            <div>
                {/* Time picker for closed from time */}
                <TimePicker
                    className='time-picker'
                    id={`${day}-closed-from`}
                    onChange={setClosedFromTime}
                    value={closedFromTime}
                    disabled={!isClosed}
                    locale='de-de'
                />
            </div>
            <div>
                {/* Time picker for closed to time */}
                <TimePicker
                    className='time-picker'
                    id={`${day}-closed-to`}
                    onChange={setClosedToTime}
                    value={closedToTime}
                    disabled={!isClosed}
                    locale='de-de'
                />
            </div>
        </div>
    );
};

export default DayRow;
