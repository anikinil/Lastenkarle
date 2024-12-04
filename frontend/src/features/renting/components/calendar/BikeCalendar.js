// Calendar for page of a singular bike
// TODO: Reservation Calendar with two months in advance view
// TODO: Legend for Colours (available, booked, closed, unavailable)
import React, { useState } from 'react';
import './BikeCalendar.css'; // CSS für die Farblegende

const getDaysInMonth = (month, year) => {
    return new Date(year, month + 1, 0).getDate();
};

const BikeCalendar = () => {
    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();

    const [selectedStartDate, setSelectedStartDate] = useState(null);
    const [selectedEndDate, setSelectedEndDate] = useState(null);
    const [availability, setAvailability] = useState({
        // Beispiel-Daten für die Verfügbarkeit (0 = buchbar, 1 = reserviert, 2 = geschlossen, 3 = nicht buchbar)
        '2024-11-06': 0,
        '2024-11-07': 1,
        '2024-11-08': 3,
        '2024-11-09': 0,
        '2024-11-10': 0,
        '2024-11-11': 0,
        '2024-11-12': 0,
        '2024-11-13': 0,
        '2024-11-14': 0,
        '2024-11-15': 0,
        '2024-11-16': 0,
        '2024-11-17': 0,
        '2024-11-18': 0
        // Weitere Verfügbarkeiten
    });

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
            } else {
                setSelectedStartDate(date);
            }
        }
    };

    const renderCalendarDays = (month, year) => {
        const daysInMonth = getDaysInMonth(month, year);
        const daysArray = Array.from({ length: daysInMonth }, (_, i) => new Date(year, month, i + 1));

        return daysArray.map((day) => {
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
        });
    };

    return (
        <div className="booking-calendar">
            <div className="month-container">
                <h2>Aktueller Monat {currentMonth + 1} {currentYear}</h2>
                <div className="calendar-grid">
                    {renderCalendarDays(currentMonth, currentYear)}
                </div>
            </div>

            <div className="month-container">
                <h2>Nächster Monat {currentMonth + 2} {currentYear}</h2>
                <div className="calendar-grid">
                    {renderCalendarDays(currentMonth + 1, currentYear)}
                </div>
            </div>

            <div className="selection-info">
                <p>Abholung: {selectedStartDate ? selectedStartDate.toDateString() : "Bitte wählen Sie ein Datum"}</p>
                <p>Rückgabe: {selectedEndDate ? selectedEndDate.toDateString() : "Bitte wählen Sie ein Datum"}</p>
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