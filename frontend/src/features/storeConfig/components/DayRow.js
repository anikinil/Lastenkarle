import React, { useState } from 'react';
import Switch from '../../../components/switch/Switch';
import TimePicker from 'react-time-picker';
import 'react-time-picker/dist/TimePicker.css';
import '../../../components/timePicker/TimePickerCustom.css'

import { useTranslation } from 'react-i18next';

const DayRow = ({ day }) => {

    const { t } = useTranslation();

    const [isOpen, setIsOpen] = useState(false);
    // const [fromTime, setFromTime] = useState(t('default_from_time'));
    // const [toTime, setToTime] = useState(t('default_to_time'));
    const [fromTime, setFromTime] = useState('10:00');
    const [toTime, setToTime] = useState('13:00');

    return (
        <div className='day-row'>
            <span className="day-label">{day}</span>
            <Switch className='opening-times-toggle' id={day} isOn={isOpen} handleToggle={() => setIsOpen(!isOpen)} />
            <div className='time-picker-container'>
                <TimePicker
                    className='time-picker'
                    id={`${day}-from`}
                    onChange={setFromTime}
                    value={fromTime}
                    disabled={!isOpen}
                />
            </div>
            <div className='time-picker-container'>
                <TimePicker
                    className='time-picker'
                    id={`${day}-to`}
                    onChange={setToTime}
                    value={toTime}
                    disabled={!isOpen}
                />
            </div>
        </div>
    );
};

export default DayRow;
