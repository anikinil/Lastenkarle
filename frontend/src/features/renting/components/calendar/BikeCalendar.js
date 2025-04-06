import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import './BikeCalendar.css';
import i18n from 'i18next';

import { useNotification } from '../../../../components/notifications/NotificationContext';
import { getCookie } from '../../../../services/Cookies';

const getDaysInMonth = (month, year) => new Date(year, month + 1, 0).getDate();
const getCurrLang = () => i18n.language;

const BikeCalendar = ({ bikeId, availabilities }) => {
    const { t } = useTranslation();
    const { showNotification } = useNotification();

    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();

    const token = getCookie('token');

    const [selectedStartDate, setSelectedStartDate] = useState(null);
    const [selectedEndDate, setSelectedEndDate] = useState(null);

    const handleDayClick = (date) => {
        const dateString = date.toISOString().split('T')[0];

        if (availabilities[dateString] !== 0) return;

        if (!selectedStartDate || (selectedStartDate && selectedEndDate)) {
            setSelectedStartDate(date);
            setSelectedEndDate(null);
        } else if (selectedStartDate && !selectedEndDate) {
            if (date >= selectedStartDate) {
                setSelectedEndDate(date);
            } else {
                setSelectedStartDate(date);
            }
        }
    };

    const postBooking = async () => {
        if (!selectedStartDate || !selectedEndDate) {
            showNotification(t('select_dates_first'), 'error');
            return;
        }

        const payload = {
            begin: selectedStartDate.toISOString().split('T')[0],
            end: selectedEndDate.toISOString().split('T')[0],
            equipment: []
        };

        try {
            const response = await fetch(`/api/booking/v1/bikes/${bikeId}/booking`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                showNotification(t('booking_successful'), 'success');
                setSelectedStartDate(null);
                setSelectedEndDate(null);
            } else {
                const error = await response.json();
                throw new Error(error.detail);
            }
        } catch (error) {
            showNotification(`${t('booking_failed')}: ${error.message}`, 'error');
        }
    };

    const isAvailableOnDate = (date) => {
        const normalizeDate = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate());
        const normalizedDate = normalizeDate(date);

        return !availabilities.some(availability => {
            const start = normalizeDate(new Date(availability.from_date));
            const end = normalizeDate(new Date(availability.until_date));
            return normalizedDate >= start && normalizedDate <= end;
        });
    };

    const renderCalendarDays = (month, year) => {
        const daysInMonth = getDaysInMonth(month, year);
        const firstDay = new Date(year, month, 1).getDay();
        const firstDayIndex = firstDay === 0 ? 6 : firstDay - 1;
        const daysArray = Array.from({ length: daysInMonth }, (_, i) => new Date(year, month, i + 1));

        return (
            <>
                {["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"].map((d, i) => (
                    <div key={i} className="weekday-label">{d}</div>
                ))}
                {Array.from({ length: firstDayIndex }).map((_, i) => (
                    <div key={`empty-${i}`} className="calendar-day empty"></div>
                ))}
                {daysArray.map((day) => {
                    const dateString = day.toISOString().split('T')[0];
                    const isSelectedStart = selectedStartDate?.toISOString().split('T')[0] === dateString;
                    const isSelectedEnd = selectedEndDate?.toISOString().split('T')[0] === dateString;

                    let dayClass = '';
                    if (day < today - 24*60*60*1000) dayClass = 'past';
                    else if (isAvailableOnDate(day)) dayClass = 'available';
                    else dayClass = 'not-bookable';

                    if (isSelectedStart || isSelectedEnd) {
                        dayClass += ' selected';
                    }

                    return (
                        <div
                            key={dateString}
                            className={`calendar-day ${dayClass}`}
                            onClick={() => handleDayClick(day)}
                        >
                            {day.getDate()}
                        </div>
                    );
                })}
            </>
        );
    };

    return (
        <div className="booking-calendar">
            <div className="month-container-wrapper">
                <div className="month-container">
                    <h2>{new Date(currentYear, currentMonth).toLocaleString(getCurrLang(), { month: 'long' })} {currentYear}</h2>
                    <div className="calendar-grid">
                        {renderCalendarDays(currentMonth, currentYear)}
                    </div>
                </div>

                <div className="month-container">
                    <h2>{new Date(currentYear, currentMonth + 1).toLocaleString(getCurrLang(), { month: 'long' })} {currentYear}</h2>
                    <div className="calendar-grid">
                        {renderCalendarDays(currentMonth + 1, currentYear)}
                    </div>
                </div>
            </div>

            <div className="selection-info">
                <p>{t('pickup_date')}: {selectedStartDate ? selectedStartDate.toDateString() : t('select_date')}</p>
                <p>{t('return_date')}: {selectedEndDate ? selectedEndDate.toDateString() : t('select_date')}</p>
            </div>

            <div className="legend">
                <p><span className="legend-color available"></span> Buchbar</p>
                <p><span className="legend-color not-bookable"></span> Nicht buchbar</p>
            </div>

            <button onClick={postBooking} className="booking-button">
                {t('book_now')}
            </button>
        </div>
    );
};

export default BikeCalendar;