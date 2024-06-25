import React, { useState } from 'react';
import Switch from '../../../components/switch/Switch';
import TimePicker from 'react-time-picker';
import 'react-time-picker/dist/TimePicker.css';
import '../../../components/timePicker/TimePickerCustom.css'

import { useTranslation } from 'react-i18next';

const DayRow = ({ day }) => {

    const { t } = useTranslation();

    const [isOpen, setIsOpen] = useState(false);
    const [isClosed, setIsClosed] = useState(false);
    
    const [openFromTime, setOpenFromTime] = useState(t('placeholder_open_from_time'));
    const [openToTime, setOpenToTime] = useState(t('placeholder_open_to_time'));
    const [closedFromTime, setClosedFromTime] = useState(t('placeholder_closed_from_time'));
    const [closedToTime, setClosedToTime] = useState(t('placeholder_closed_to_time'));

    const handleOpenToggle = () => {
        if (isOpen) { setIsClosed(false) }
        setIsOpen(!isOpen)
    }

    const handleClosedToggle = () => {
        setIsClosed(!isClosed)
    }

    return (
        <div className='day-row'>
            <span className="day-label">{day}</span>
            <Switch className='opening-times-toggle' id={`${day}-open`} isOn={isOpen} handleToggle={handleOpenToggle} disabled={false}/>
            <div className='time-picker-container'>
                <TimePicker
                    className='time-picker'
                    id={`${day}-open-from`}
                    onChange={setOpenFromTime}
                    value={openFromTime}
                    disabled={!isOpen}
                />
            </div>
            <div className='time-picker-container'>
                <TimePicker
                    className='time-picker'
                    id={`${day}-open-to`}
                    onChange={setOpenToTime}
                    value={openToTime}
                    disabled={!isOpen}
                />
            </div>
            <Switch className='opening-times-toggle' id={`${day}-closed`} isOn={isClosed} handleToggle={handleClosedToggle} disabled={!isOpen}/>
            <div className='time-picker-container'>
                <TimePicker
                    className='time-picker'
                    id={`${day}-closed-from`}
                    onChange={setClosedFromTime}
                    value={closedFromTime}
                    disabled={!isClosed}
                />
            </div>
            <div className='time-picker-container'>
                <TimePicker
                    className='time-picker'
                    id={`${day}-closed-to`}
                    onChange={setClosedToTime}
                    value={closedToTime}
                    disabled={!isClosed}
                />
            </div>
        </div>
    );
};

export default DayRow;
