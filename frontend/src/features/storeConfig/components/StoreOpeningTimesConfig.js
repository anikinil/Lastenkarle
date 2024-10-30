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
                    <DayRow key={day} day={day} />
                ))}
            </div>
        </>
    );
};

export default StoreOpeningTimesConfig;