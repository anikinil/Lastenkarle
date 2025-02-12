// Calendar for page of a singular bike
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import './BikeCalendar.css'; // CSS für die Farblegende
import i18n from 'i18next';

const getDaysInMonth = (month, year) => {
    return new Date(year, month + 1, 0).getDate();
};

const getCurrLang = () => {
    return i18n.language
}

const generateDefaultAvailability = (year, month) => {
    const daysInMonth = getDaysInMonth(month, year);
    const availability = {};
    
    for (let day = 1; day <= daysInMonth; day++) {
        const dateString = new Date(year, month, day).toISOString().split('T')[0];
        availability[dateString] = 0; // Default all days to 'available' (0)
    }

    return availability;
};

const BikeCalendar = () => {


    const { t } = useTranslation(); // Translation hook
    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();

    const [selectedStartDate, setSelectedStartDate] = useState(null);
    const [selectedEndDate, setSelectedEndDate] = useState(null);
    const [availability, setAvailability] = useState(generateDefaultAvailability(currentYear, currentMonth));


    const handleDayClick = (date) => {
        const dateString = date.toISOString().split('T')[0];

        if (availability[dateString] !== 0) {
            // Tag nicht buchbar
            return;
        }

        if (!selectedStartDate || (selectedStartDate && selectedEndDate)) {
            setSelectedStartDate(date);
            setSelectedEndDate(null);
        } else if (selectedStartDate && !selectedEndDate) {
            if (date >= selectedStartDate) {
                setSelectedEndDate(date);
            }
            if (date <= selectedStartDate){
                setSelectedStartDate(date);
            }
        }

    };

    const renderCalendarDays = (month, year) => {
        const daysInMonth = getDaysInMonth(month, year);
        const firstDayOfMonth = new Date(year, month, 1).getDay(); // Get the weekday index (0 = Sunday, 1 = Monday, etc.)
    
        // Convert Sunday (0) to be the last day instead (aligning Monday as the first day)
        const firstDayIndex = firstDayOfMonth === 0 ? 6 : firstDayOfMonth - 1;
    
        const daysArray = Array.from({ length: daysInMonth }, (_, i) => new Date(year, month, i + 1));
    
        return (
            <>
                {/* Weekday Labels */}
                {["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"].map((day, index) => (
                    <div key={index} className="weekday-label">{day}</div>
                ))}
    
                {/* Empty slots for alignment */}
                {Array.from({ length: firstDayIndex }).map((_, i) => (
                    <div key={`empty-${i}`} className="calendar-day empty"></div>
                ))}
    
                {/* Actual days */}
                {daysArray.map((day) => {
                    const dateString = day.toISOString().split('T')[0];
                    const isSelectedStart = selectedStartDate && selectedStartDate.toISOString().split('T')[0] === dateString;
                    const isSelectedEnd = selectedEndDate && selectedEndDate.toISOString().split('T')[0] === dateString;
    
                    let dayClass = '';
                    if (availability[dateString] === 0) {
                        dayClass = 'available';
                    } else if (availability[dateString] === 1) {
                        dayClass = 'reserved';
                    } else if (availability[dateString] === 2) {
                        dayClass = 'closed';
                    } else {
                        dayClass = 'not-bookable';
                    }
    
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
                <p>{t('return_date')}: {selectedEndDate ? selectedEndDate.toDateString(): t('select_date')}</p>
            </div>

            <div className="legend">
                <p><span className="legend-color available"></span> Buchbar</p>
                <p><span className="legend-color reserved"></span> Reserviert</p>
                <p><span className="legend-color closed"></span> Standort geschlossen</p>
                <p><span className="legend-color not-bookable"></span> Nicht buchbar</p>
            </div>
        </div>

    );
};

export default BikeCalendar;