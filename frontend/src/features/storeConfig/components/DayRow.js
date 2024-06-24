import React, { useState } from 'react';
import Switch from '../../../components/UI/Switch';
import { TimePicker } from 'antd';

import { useTranslation } from 'react-i18next';

const DayRow = ({ day }) => {

    const { t } = useTranslation();

    const [isOpen, setIsOpen] = useState(false);
    // const [fromTime, setFromTime] = useState(t('default_from_time'));
    // const [toTime, setToTime] = useState(t('default_to_time'));
    const [fromTime, setFromTime] = useState('10:00');
    const [toTime, setToTime] = useState('18:00');

    return (
        <div className="day-row">
            <span className="day-label">{day}</span>
            <Switch className='toggle' isOn={isOpen} handleToggle={() => setIsOpen(!isOpen)} />
            <TimePicker className='time-picker' onChange={setFromTime} disabled={!isOpen} />
            <TimePicker className='time-picker' onChange={setToTime} disabled={!isOpen} />
        </div>
    );
};

export default DayRow;
