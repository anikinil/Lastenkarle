// Component used to config opening times of a store
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import DayRow from './DayRow';

import './StoreOpeningTimesConfig.css'
import 'react-time-picker/dist/TimePicker.css';
// import 'react-clock/dist/Clock.css';

const StoreOpeningTimesConfig = () => {
    // Hook for translation
    const { t } = useTranslation();

    // Array of days of the week translated
    const daysOfWeek = [t('monday'), t('tuesday'), t('wednesday'), t('thursday'), t('friday'), t('saturday'), t('sunday')];

    const [openingTimes, setOpeningTimes] = useState({
        monday: { open: false, from: '00:00', to: '00:00', closed: false, from: '00:00', to: '00:00' },
        tuesday: { open: false, from: '00:00', to: '00:00', closed: false, from: '00:00', to: '00:00' },
        wednesday: { open: false, from: '00:00', to: '00:00', closed: false, from: '00:00', to: '00:00' },
        thursday: { open: false, from: '00:00', to: '00:00', closed: false, from: '00:00', to: '00:00' },
        friday: { open: false, from: '00:00', to: '00:00', closed: false, from: '00:00', to: '00:00' },
        saturday: { open: false, from: '00:00', to: '00:00', closed: false, from: '00:00', to: '00:00' },
        sunday: { open: false, from: '00:00', to: '00:00', closed: false, from: '00:00', to: '00:00' }
    });

    const handleDayChange = (day, open, from, to, closed, fromClosed, toClosed) => {
        setOpeningTimes({
            ...openingTimes,
            [day]: { open, from, to, closed, fromClosed, toClosed }
        });
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
                    <span className='header-label'>{t('closed')}</span>
                    <span className='header-label'>{t('from')}</span>
                    <span className='header-label'>{t('to')}</span>
                </div>
                {/* Render a DayRow component for each day of the week */}
                {daysOfWeek.map((day) => (
                    <DayRow key={day} day={day} onChange={handleDayChange}/>
                ))}
            </div>
        </>
    );
};

export default StoreOpeningTimesConfig;