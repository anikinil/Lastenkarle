import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import './BikeCalendar.css';
import i18n from 'i18next';

// TODO also display closed and reseved days (needs to be fetched seperately)
// TODO add legend for closed and reserved days

const getDaysInMonth = (month, year) => new Date(year, month + 1, 0).getDate();
const getCurrLang = () => i18n.language;

const BikeCalendar = ({ storeOpeningDays, availabilities, selectedStartDate, setSelectedStartDate, selectedEndDate, setSelectedEndDate }) => {
    const { t } = useTranslation();

    console.log('storeOpeningDays', storeOpeningDays);

    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();

    const [start, setStart] = useState(selectedStartDate);
    const [end, setEnd] = useState(selectedEndDate);

    const handleDayClick = (date) => {

        if (!selectedStartDate || (selectedStartDate && selectedEndDate)) {
            setStart(date);
            setSelectedStartDate(date);
            setEnd(null);
            setSelectedEndDate(null);
        } else if (selectedStartDate && !selectedEndDate) {
            if (date >= selectedStartDate) {
                setEnd(date);
                setSelectedEndDate(date);
            } else {
                setStart(date);
                setSelectedStartDate(date);
            }
        }
    };

    const isStoreOpen = (date) => {
        const weekday = date.toLocaleDateString('en-US', { weekday: 'short' }).toLowerCase();
        return storeOpeningDays[weekday] === true;
    }

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
            <div className="calendar-grid">
                {/* TODO make weekdays translatable */}
                {/* Weekday labels (top row) */}
                {["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"].map((d, i) => (
                    <div key={`label-${i}`} className="weekday-label">{d}</div>
                ))}

                {/* Empty slots before the first day of the month */}
                {Array.from({ length: firstDayIndex }).map((_, i) => (
                    <div key={`empty-${i}`} className="calendar-day empty"></div>
                ))}

                {/* Actual days */}
                {daysArray.map((day) => {
                    const dateString = day.toLocaleDateString('en-CA') // format date to 'YYYY-MM-DD'
                    const isSelectedStart = start?.toLocaleDateString('en-CA') === dateString;
                    const isSelectedEnd = end?.toLocaleDateString('en-CA') === dateString;
                    const isInRange = start && end && day >= start && day <= end;
                    let dayClass = '';

                    if (day < new Date(today.getTime() - 24 * 60 * 60 * 1000)) {
                        dayClass = 'past';
                    } else if (!isStoreOpen(day)) {
                        dayClass = 'closed';
                    } else if (isAvailableOnDate(day)) {
                        dayClass = 'available';
                    } else {
                        dayClass = 'booked';
                    }

                    if (isInRange || isSelectedStart || isSelectedEnd) {
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
            </div>
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
                <p><span className="legend-color available"></span>{t('bookable')}</p>
                <p><span className="legend-color not-bookable"></span>{t('not_bookable')}</p>
            </div>
        </div>
    );
};

export default BikeCalendar;