// Component used to config opening times of a store
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import DayRow from './DayRow';
import TimePicker from 'react-time-picker';

import './StoreOpeningTimesConfig.css'
import 'react-time-picker/dist/TimePicker.css';
import '../timePicker/TimePickerCustom.css';

// NOTE remove
// const defaultOpeningTimes = {
//     monday: { open: false, from: '00:00', to: '00:00', closed: false, from: '00:00', to: '00:00' },
//     tuesday: { open: false, from: '00:00', to: '00:00', closed: false, from: '00:00', to: '00:00' },
//     wednesday: { open: false, from: '00:00', to: '00:00', closed: false, from: '00:00', to: '00:00' },
//     thursday: { open: false, from: '00:00', to: '00:00', closed: false, from: '00:00', to: '00:00' },
//     friday: { open: false, from: '00:00', to: '00:00', closed: false, from: '00:00', to: '00:00' },
//     saturday: { open: false, from: '00:00', to: '00:00', closed: false, from: '00:00', to: '00:00' },
//     sunday: { open: false, from: '00:00', to: '00:00', closed: false, from: '00:00', to: '00:00' }
// }

const StoreOpeningTimesConfig = ({prepareTimeValue, openingTimesValue, onPrepareTimeChange, onOpeningTimesChange}) => {
    // Hook for translation
    const { t } = useTranslation();

    // Array of days of the week translated
    const daysOfWeek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];

    const [prepareTime, setPrepareTime] = useState(prepareTimeValue);
    const [openingTimes, setOpeningTimes] = useState(openingTimesValue);

    // const handleDayChange = (day, open, from, to) => {
    //     let change = {
    //         ...openingTimes,
    //         // [day]: { open, from, to, closed, fromClosed, toClosed }
    //         [day]: { open, from, to}
    //     }
    //     setOpeningTimes(change);
    //     onOpeningTimesChange(change);
    // }

    const handleOpenChange = (day, open) => {
        let change = {
            ...openingTimes,
            [day]: { ...openingTimes[day], open }
        }
        setOpeningTimes(change);
        onOpeningTimesChange(change);
    }

    const handleFromChange = (day, from) => {
        let change = {
            ...openingTimes,
            [day]: { ...openingTimes[day], from }
        }
        console.log("DAY");
        console.log(day);
        console.log("CHANGE");
        console.log(change);
        setOpeningTimes(change);
        onOpeningTimesChange(change);
    }

    const handleToChange = (day, to) => {
        let change = {
            ...openingTimes,
            [day]: { ...openingTimes[day], to }
        }
        setOpeningTimes(change);
        onOpeningTimesChange(change);
    }

    const handlePrepareTimeChange = (time) => {
        setPrepareTime(time);
        onPrepareTimeChange(time);
    }
    
    return (
        <>
            {/* Heading for the opening times section */}
            <h2>{t('opening_times')}</h2>

            <div className='prepare-time-container'>
                <span>{t('prepare_time')}</span>
                <div>
                    {/* Time picker for open from time */}
                    <TimePicker
                        className='time-picker'
                        id={`prepare-time`}
                        onChange={handlePrepareTimeChange}
                        value={prepareTime}
                        locale='de-de'
                    />
                </div>
            </div>

            <div className='week-container'>
                {/* Header row for the table */}
                <div className='header'>
                    <span className='header-label'></span> {/* empty on purpose */}
                    <span className='header-label'>{t('open')}</span>
                    <span className='header-label'>{t('from')}</span>
                    <span className='header-label'>{t('to')}</span>
                    {/* <span className='header-label'>{t('closed')}</span>
                    <span className='header-label'>{t('from')}</span>
                    <span className='header-label'>{t('to')}</span> */}
                </div>
                {/* Render a DayRow component for each day of the week */}
                {daysOfWeek.map((day, index) => (
                    <DayRow 
                        key={index} 
                        day={t(day)} 
                        onOpenChange={(open) => handleOpenChange(day, open)} 
                        onFromChange={(from) => handleFromChange(day, from)} 
                        onToChange={(to) => handleToChange(day, to)} 
                    />
                ))}
            </div>
        </>
    );
};

export default StoreOpeningTimesConfig;