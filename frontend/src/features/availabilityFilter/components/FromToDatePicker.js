
import React from 'react';

import './FromToDatePicker.css';

import { useTranslation } from 'react-i18next';

const FromToDatePicker = ({ from, to, setFrom, setTo }) => {

    const { t } = useTranslation();

    return (
        <div className="from-to-date-picker-container">

            <div className="date-container">
                <label htmlFor="from">{t('from')}: </label>
                <input
                    className='datepicker-input'
                    type="date"
                    id="from"
                    name="from"
                    value={from}
                    onChange={(e) => setFrom(e.target.value)}>
                </input>
            </div>

            <div className="date-container">
                <label htmlFor="to">{t('to')}: </label>
                <input
                    className='datepicker-input'
                    type="date"
                    id="to"
                    name="to"
                    value={to}
                    onChange={(e) => setTo(e.target.value)}
                ></input>
            </div>

            <button className="filter-button">{t('filter')}</button>
        </div>
    );
}

export default FromToDatePicker;