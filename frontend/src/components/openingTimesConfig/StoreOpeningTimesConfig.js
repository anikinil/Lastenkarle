// Component used to config opening times of a store
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import DayRow from './DayRow';
import TimePicker from 'react-time-picker';

import './StoreOpeningTimesConfig.css'
import 'react-time-picker/dist/TimePicker.css';
import '../timePicker/TimePickerCustom.css';

const StoreOpeningTimesConfig = ({ prepareTimeValue, openingTimesValue, onPrepareTimeChange, onOpeningTimesChange }) => {
    // Hook for translation
    const { t } = useTranslation();

    const daysOfWeek = [
        { long: 'monday', short: 'mon' },
        { long: 'tuesday', short: 'tue' },
        { long: 'wednesday', short: 'wed' },
        { long: 'thursday', short: 'thu' },
        { long: 'friday', short: 'fri' },
        { long: 'saturday', short: 'sat' },
        { long: 'sunday', short: 'sun' }];

    const [prepareTime, setPrepareTime] = useState(prepareTimeValue);
    const [openingTimes, setOpeningTimes] = useState(openingTimesValue);

    const handleOpenChange = (day, open) => {
        console.log(openingTimes)

        let change = {
            ...openingTimes,
            [day.short + '_opened']: open
        }
        setOpeningTimes(change);
        onOpeningTimesChange(change);
    }

    const handleFromChange = (day, from) => {
        let change = {
            ...openingTimes,
            [day.short + '_open']: from
        }
        setOpeningTimes(change);
        onOpeningTimesChange(change);
    }

    const handleToChange = (day, to) => {
        let change = {
            ...openingTimes,
            [day.short + '_close']: to
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

            <div className='week-container'>
                {/* Header row for the table */}
                <div className='header'>
                    <span className='header-label'></span> {/* empty on purpose */}
                    <span className='header-label'>{t('open')}</span>
                    <span className='header-label'>{t('from')}</span>
                    <span className='header-label'>{t('to')}</span>
                </div>
                {/* Render a DayRow component for each day of the week */}
                {daysOfWeek.map((day, index) => (
                    <DayRow
                        key={index}
                        day={t(day.long)}
                        isOpenValue={openingTimes[day.short + '_opened']}
                        fromValue={openingTimes[day.short + '_open']}
                        toValue={openingTimes[day.short + '_close']}
                        onOpenChange={(open) => handleOpenChange(day, open)}
                        onFromChange={(from) => handleFromChange(day, from)}
                        onToChange={(to) => handleToChange(day, to)}
                    />
                ))}
            </div>

            <div className='prepare-time-container'>
                <p>{t('prepare_time')}</p>
                {/* Time picker for open from time */}
                <TimePicker
                    className='time-picker'
                    id={`prepare-time`}
                    onChange={handlePrepareTimeChange}
                    value={prepareTime}
                    format='HH:mm'
                    locale='de-de'
                />
            </div>
        </>
    );
};

export default StoreOpeningTimesConfig;