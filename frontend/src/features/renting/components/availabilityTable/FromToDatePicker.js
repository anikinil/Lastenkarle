
import React from 'react';

import './FromToDatePicker.css';

import { useTranslation } from 'react-i18next';

import { useState, useEffect } from 'react';
import { useNotification } from '../../../../components/notifications/NotificationContext';

const FromToDatePicker = ({ from, to, setFrom, setTo}) => {

    const { t } = useTranslation();

    const { showNotification } = useNotification();

    const [fromVal, setFromVal] = useState('');
    const [toVal, setToVal] = useState('');

    const handleResetClick = () => {
        setFrom('');
        setTo('');
    };

    useEffect(() => {
        if (fromVal && toVal && fromVal > toVal) {
            showNotification(t('from-must-be-before-to'), 'error');
        } else {
            setFrom(fromVal);
        }
    }, [fromVal]);

    useEffect(() => {
        if (fromVal && toVal && fromVal > toVal) {
            showNotification(t('from-must-be-before-to'), 'error');
        } else {
            setTo(toVal);
        }
    }, [toVal]);
    

    return (
        <div className="from-to-date-picker-container">

            <div className="date-container">
                <label htmlFor="from">{t('from')}</label>
                <input
                    className='datepicker-input'
                    type="date"
                    id="from"
                    name="from"
                    value={from}
                    onChange={(e) => setFromVal(e.target.value)}>
                </input>
            </div>

            <div className="date-container">
                <label htmlFor="to">{t('to')}</label>
                <input
                    className='datepicker-input'
                    type="date"
                    id="to"
                    name="to"
                    value={to}
                    onChange={(e) => setToVal(e.target.value)}
                ></input>
            </div>

            <button className="reset-button" onClick={handleResetClick}>{t('reset')}</button>
        </div>
    );
}

export default FromToDatePicker;